from random import randint
import random
import datetime

class TPCH_HELPER:

    def __init__(self):
        self.region_list = ['AFRICA', 'AMERICA', 'ASIA', 'EUROPE', 'MIDDLE EAST']
        self.nation_list = ['ALGERIA', 'ARGENTINA', 'BRAZIL', 'CANADA', 'EGYPT', 'ETHIOPIA', 'FRANCE', 'GERMANY', 'INDIA', 'INDONESIA', 'IRAN', 'IRAQ', 'JAPAN', 'JORDAN', 'KENYA', 'MOROCCO', 'MOZAMBIQUE', 'PERU', 'CHINA', 'ROMANIA', 'SAUDI ARABIA', 'VIETNAM', 'RUSSIA', 'UNITED KINGDOM', 'UNITED STATES']
        self.type_list = ['TIN', 'NICKEL', 'BRASS', 'STEEL', 'COPPER']
        self.segment_list = ['AUTOMOBILE', 'BUILDING', 'FURNITURE', 'MACHINERY', 'HOUSEHOLD']
        self.color_list = ['RED', 'BLUE', 'YELLOW', 'ORANGE', 'BROWN', 'PINK', 'WHITE', 'BLACK']
        self.ship_model_list1  = ['STANDARD', 'SMALL', 'MEDIUM', 'LARGE', 'ECONOMY', 'PROMO']
        self.ship_model_list2  = ['ANODIZED', 'BURNISHED', 'PLATED', 'POLISHED', 'BRUSHED']
        self.ship_model_list3  = ['TIN', 'NICKEL', 'BRASS', 'STEEL', 'COPPER']
        self.word1_list = ['SPECIAL','PENDING','UNUSUAL','EXPRESS']
        self.word2_list = ['PACKAGES','REQUESTS','ACCOUNTS','DEPOSITS']
        self.letters_list = ['A','B','C','D','E','F']
        self.date1 = None
        self.date2 = None
        self.number = 0
        self.region = ''
        self.nation = ''
        self.type = ''
        self.segment = ''

    def random_date(self, start_date_str, end_date_str):
        low_bound = 0
        start_date = datetime.datetime.strptime(start_date_str, '%Y%m%d').date()
        end_date = datetime.datetime.strptime(end_date_str, '%Y%m%d').date()
        upper_bound = abs((end_date - start_date).days)
        self.date1 = start_date + datetime.timedelta(days=(random.randint(int(low_bound), int(upper_bound))))
        return self.date1

    def random_date_plus(self, days_added):
        self.date2 = self.date1 + datetime.timedelta(days=int(days_added))
        return self.date2

    def random_date_year(self, lower_bound, upper_bound):
        rand_year = self.random_int(lower_bound, upper_bound)
        date_str = str(rand_year) + '0101'
        self.date1 = datetime.datetime.strptime(date_str, '%Y%m%d').date()
        return self.date1

    def random_int(self, lower_bound, upper_bound):
        self.number = random.randint(lower_bound, upper_bound)
        return self.number

    def random_float(self, lower_bound, upper_bound):
        self.number = random.uniform(lower_bound, upper_bound)
        return self.number

    def random_element(self, list_name):
        element = ''
        if list_name == 'region_list':
            element = self.region_list[randint(0,len(self.region_list)-1)]
            self.region = element
        elif list_name == 'type_list':
            element = self.type_list[randint(0,len(self.type_list)-1)]
            self.type = element
        elif list_name == 'nation_list':
            element = self.nation_list[randint(0,len(self.nation_list)-1)]
            self.nation = element
        elif list_name == 'segment_list':
            element = self.segment_list[randint(0,len(self.segment_list)-1)]
            self.segment = element
        elif list_name == 'color_list':
            element = self.color_list[randint(0,len(self.color_list)-1)]
            self.color = element
        elif list_name == 'ship_model_list1':
            element = self.ship_model_list1[randint(0,len(self.ship_model_list1)-1)]
            self.ship_model1 = element
        elif list_name == 'ship_model_list2':
            element = self.ship_model_list2[randint(0,len(self.ship_model_list2)-1)]
            self.ship_model2 = element
        elif list_name == 'ship_model_list3':
            element = self.ship_model_list3[randint(0,len(self.ship_model_list3)-1)]
            self.ship_model3 = element
        elif list_name == 'word1_list':
            element = self.word1_list[randint(0,len(self.word1_list)-1)]
            self.word1 = element
        elif list_name == 'word2_list':
            element = self.word2_list[randint(0,len(self.word2_list)-1)]
            self.word2 = element
        elif list_name == 'letters_list':
            element = self.letters_list[randint(0,len(self.letters_list)-1)]
            self.letters = element
        elif list_name == 'type_list1':
            element = self.ship_model_list3[randint(0,len(self.ship_model_list3)-1)]
            element = element[:3]
            self.type3 = element
        return element

    def replace_qstr(self, qstr, replace_str, new_str):
        temp_replace_str = '<parse_value>' + replace_str + '</parse_value>'
        temp_new_str =  qstr.replace(temp_replace_str, new_str)
        return temp_new_str
