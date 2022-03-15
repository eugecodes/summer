from sqlalchemy import Numeric, Column, Unicode, DateTime, func, ForeignKey, Integer, Table, Text, PrimaryKeyConstraint, String, \
    Sequence, create_engine
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import relationship, column_property, relationship, backref, scoped_session, sessionmaker
from worldbank.model import DeclarativeBase

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from StringIO import StringIO
from sqlalchemy.ext.hybrid import hybrid_property
	
import flask.ext.sqlalchemy
import flask.ext.restless

class ModelMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=func.now())

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, onupdate=func.now())

    def __init__(self, **kwargs):
            cls = self.__class__
            for key in kwargs:
                if not hasattr(cls, key):
                    raise TypeError(
                        "%r is an invalid keyword argument for %s" %
                        (key, cls.__name__))
                setattr(self, key, kwargs[key])


class Region(DeclarativeBase, ModelMixin):
    id = Column(Unicode(5), primary_key=True)
    iso2code = Column(Unicode(2))
    name = Column(Unicode(128))

    countries = relationship("Country", foreign_keys="Country.regionId", back_populates="region")
    adminedCountries = relationship("Country", foreign_keys="Country.adminRegionId", back_populates="adminRegion")

    indicatorsData = relationship("IndicatorRegion", back_populates="region")

    def __repr__(self):
        return "<%s(id='%s', name='%s')>" % (self.__class__.__name__, self.id, self.name)


class IncomeLevel(DeclarativeBase, ModelMixin):
	__tablename__ = 'income_level'
	id = Column(Unicode(5), primary_key=True)
	value = Column(Unicode(128))
	countries = relationship("Country", backref=backref('country'))
	indicatorsData = relationship("IndicatorIncomeLevel", back_populates="incomeLevel")
	def __repr__(self):
		return "<%s(id='%s', value='%s')>" % (self.__class__.__name__, self.id, self.value)


class LendingType(DeclarativeBase, ModelMixin):
	__tablename__ = 'lending_type'
	id = Column(Unicode(5), primary_key=True)
	value = Column(Unicode(64))
	#countries = relationship("Country", back_populates="lendingType")
	#countries = relationship("Country", backref=backref('country'))
	def __repr__(self):
		return "<%s(id='%s', value='%s')>" % (self.__class__.__name__, self.id, self.value)


class Country(DeclarativeBase, ModelMixin):
    id = Column(Unicode(2), primary_key=True)
    iso2code = Column(Unicode(2), unique=True)
    iso3code = Column(Unicode(3), unique=True)
    name = Column(Unicode(64))
    capital = Column(Unicode(64))
    longitude = Column(Numeric(precision=9, scale=6))
    latitude = Column(Numeric(precision=9, scale=6))

    regionId = Column("region_id", Unicode(5), ForeignKey("region.id"))
    region = relationship("Region", foreign_keys=regionId, back_populates="countries")

    adminRegionId = Column("admin_region_id", Unicode(5), ForeignKey("region.id"))
    adminRegion = relationship("Region", foreign_keys=adminRegionId, back_populates="adminedCountries")

    incomeLevelId = Column("income_level_id", Unicode(5), ForeignKey("income_level.id"))
    incomeLevel = relationship("IncomeLevel", foreign_keys=incomeLevelId, back_populates="countries")

    lendingTypeId = Column("lending_type_id", Unicode(5), ForeignKey("lending_type.id"))
    #lendingType = relationship("LendingType", foreign_keys=lendingTypeId, back_populates="countries")

    indicatorsData = relationship("IndicatorCountry", back_populates="country")

    def __repr__(self):
        return "<%s(id='%s', name='%s')>" % (self.__class__.__name__, self.id, self.name)


indicatorTopicTable = Table('indicator_topic', DeclarativeBase.metadata,
    Column('indicator_id', Unicode(32), ForeignKey('indicator.id')),
    Column('topic_id', Integer, ForeignKey('topic.id')),
    PrimaryKeyConstraint('indicator_id', 'topic_id', name='indicator_topic_pk')
)


class Indicator(DeclarativeBase, ModelMixin):
    id = Column(Unicode(256), primary_key=True)
    name = Column(Unicode(512))
    sourceNote = Column("source_note", Text())
    sourceOrganization = Column("source_org", Text())

    sourceId = Column("source_id", Integer, ForeignKey('source.id'))
    source = relationship("Source", foreign_keys=sourceId, back_populates="indicators")

    topics = relationship("Topic", secondary=indicatorTopicTable, back_populates="indicators")

    countriesData = relationship("IndicatorCountry", back_populates="indicator")
    regionsData = relationship("IndicatorRegion", back_populates="indicator")
    incomeLevelsData = relationship("IndicatorIncomeLevel", back_populates="indicator")

    def __repr__(self):
        return "<%s(id='%s', name='%s')>" % (self.__class__.__name__, self.id, self.name)


class Source(DeclarativeBase, ModelMixin):
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(128))
    description = Column(Unicode(512))
    url = Column(Unicode(128))

    indicators = relationship("Indicator", back_populates="source")

    def __repr__(self):
        return "<%s(id='%s', value='%s')>" % (self.__class__.__name__, self.id, self.name)


class Topic(DeclarativeBase, ModelMixin):
    id = Column(Integer, primary_key=True)
    value = Column(Unicode(128))
    sourceNote = Column("source_note", Unicode(1024))

    indicators = relationship("Indicator", secondary=indicatorTopicTable, back_populates="topics")

    def __repr__(self):
        return "<%s(id='%s', value='%s')>" % (self.__class__.__name__, self.id, self.value)


class IndicatorCountry(DeclarativeBase, ModelMixin):
    __tablename__ = 'indicator_country'
    __table_args__ = (
        PrimaryKeyConstraint('indicator_id', 'date', 'country_id', name='ind_data_cntry_pk'),
    )
    value = Column(Unicode(128))
    date = Column(Integer)

    countryId = Column("country_id", Unicode(2), ForeignKey("country.id"))
    country = relationship("Country", foreign_keys=countryId, back_populates="indicatorsData")

    indicatorId = Column("indicator_id", Unicode(256), ForeignKey("indicator.id"))
    indicator = relationship("Indicator", foreign_keys=indicatorId, back_populates="countriesData")


class IndicatorRegion(DeclarativeBase, ModelMixin):
    __tablename__ = 'indicator_region'
    __table_args__ = (
        PrimaryKeyConstraint('indicator_id', 'date', 'region_id', name='ind_data_region_pk'),
    )
    value = Column(Unicode(128))
    date = Column(Integer)

    regionId = Column("region_id", Unicode(5), ForeignKey("region.id"))
    region = relationship("Region", foreign_keys=regionId, back_populates="indicatorsData")

    indicatorId = Column("indicator_id", Unicode(256), ForeignKey("indicator.id"))
    indicator = relationship("Indicator", foreign_keys=indicatorId, back_populates="regionsData")


class IndicatorIncomeLevel(DeclarativeBase, ModelMixin):
    __tablename__ = 'indicator_income_level'
    __table_args__ = (
        PrimaryKeyConstraint('indicator_id', 'date', 'income_level_id', name='ind_data_inclevel_pk'),
    )
    value = Column(Unicode(128))
    date = Column(Integer)

    incomeLevelId = Column("income_level_id", Unicode(5), ForeignKey("income_level.id"))
    incomeLevel = relationship("IncomeLevel", foreign_keys=incomeLevelId, back_populates="indicatorsData")

    indicatorId = Column("indicator_id", Unicode(256), ForeignKey("indicator.id"))
    indicator = relationship("Indicator", foreign_keys=indicatorId, back_populates="incomeLevelsData")


class CountryIncomeLevelHistory(DeclarativeBase):
    __tablename__ = 'cntry_inclevel_hist'
    id = Column(Integer, Sequence('cntry_inclvl_seq'), primary_key=True)

    oldValueId = Column("old_value_id", Unicode(5), ForeignKey(IncomeLevel.id))
    oldValue = relationship(IncomeLevel, foreign_keys=oldValueId)

    newValueId = Column("new_value_id", Unicode(5), ForeignKey(IncomeLevel.id))
    newValue = relationship(IncomeLevel, foreign_keys=newValueId)

    created_at = Column(DateTime, default=func.now())

class CountryLendingTypeHistory(DeclarativeBase):
    __tablename__ = 'cntry_lendtype_hist'
    id = Column(Integer, Sequence('cntry_lendtype_seq'), primary_key=True)

    oldValueId = Column("old_value_id", Unicode(5), ForeignKey(LendingType.id))
    oldValue = relationship(LendingType, foreign_keys=oldValueId)

    newValueId = Column("new_value_id", Unicode(5), ForeignKey(LendingType.id))
    newValue = relationship(LendingType, foreign_keys=newValueId)

    created_at = Column(DateTime, default=func.now())
