import re
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

class Utilities():
    """ Utilities for dataset cleaning.
        
        ...

        Methods
        ------

        1. html_remover(pd.Series) -> pd.Series

        2. delete_support_message(pd.Series) -> pd.Series

        3. delete_end_of_message(pd.Series) -> pd.Series

        4. delete_numbers_with_pre(pd.Series) -> pd.Series

        5. delete_extra_puctuation(pd.Series) -> pd.Series

        6. change_spaces(pd.Series) -> pd.Series

        8. clean_text

        9. clean_names

        10. lowering

        11. delete_pp

        12. delete_links

        13. remove_emails

        14. remove_dates

    """


    DAYS_OF_WEEK: list = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота',
                        'Вск', 'Пнд', 'Втр', 'Сре', 'Чтв', 'Птн', 'Суб',
                        'Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб',
                        'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
                        'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat',
                        'Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']


    MONTHS: list = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь',
                    'Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря',
                    'Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'сент', 'Окт', 'Ноя', 'Дек',
                    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
                    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']



    def html_remover(self, text):
        beauti = BeautifulSoup(text,'lxml')#'html.parser'
        for data in beauti(['table','style', 'script', 'code', 'img', 'link', 'a']):
            data.decompose()
        return beauti.get_text('.').strip() #сюда добавила точку для разделения, чтобы слова не соединялись в одно


    def delete_support_message(self, text):
        if "@yoomoney.ru" in text:
            ind = re.search(r'[\w\.-]+@yoomoney.ru', text)
            if ind is not None:
                ind = ind.span()[0]
                text = text[:ind]
        if "@yamoney.ru" in text:
            ind = re.search(r'[\w\.-]+@yamoney.ru', text)
            if ind is not None:
                ind = ind.span()[0]
                text = text[:ind]
        return text


    
    def delete_end_of_message(self, text):
    
        """ 
        Если в сообщении есть "С уважением.."/"Отправлено из", 
        то все, что после этого, тоже можно обрезать 
        """

        if 'С уважением' in text:
            text = text[:text.find('С уважением')]
        if  "Отправлено из" in text:
            text = text[:text.find("Отправлено из")] 
        if  "Отправлено с" in text:
            text = text[:text.find("Отправлено с")] 
        if '___' in text:
            text = text[:text.find("____")] 
        if "========" in text:
            text = text[:text.find("========")] 
        if "Sent from" in text:
            text = text[:text.find("Sent from")]
        if "Best regard" in text:
            text = text[:text.find("Best regard")]
        return text
    
    def replace_account_numbers(self, text):
        return re.sub(r"4100\d{7,}", " #кошелек# ", text)

    def replace_phone_numbers(self, text):
        return re.sub(r" ((8)|(\+\d{1,3}))?[\- ]?(\(?\d{3}\)?[\- ]?)(([\d]{7})|([\d\- ]{9}))( |[:;,.!?])", " #телефон# ", text)

    def delete_numbers_with_prep(self, text):
        return re.sub(r" (\w{1,2} \d+)|([+-]?\d+)", "", text)

    def add_period(self, text):
        return re.sub(r"([\t\v\r\n\f]+)|([ ]{4})", ". ", text)

    def delete_extra_puctuation(self, text):
        #убираем --, "", <>
        text = re.sub(r"[<>\"\']|(--)", "", text)

    #если перед любым знаком препинания идет пробел, то оставляем только знак препинания
        def dashrepl1(matchobj):
            return matchobj.group()[-1]
        text = re.sub(r"\s+[,!.?:;]", dashrepl1, text)

    #убираем последовательности символов (повторения более одного раза)
        text = re.sub(r"[.]+", ".", text) #последовательности точек
        text = re.sub(r"[,]+", ",", text) #последовательности запятых
        text = re.sub(r"[!]+", "!", text) #последовательности !
        text = re.sub(r"[?]+", "?", text) #последовательности ?
        text = re.sub(r"[:]+", ":", text) #последовательности :
        text = re.sub(r"[;]+", ";", text) #последовательности ;
        text = re.sub(r"\?!", "?", text) #последовательности ?!
        text = re.sub(r"\!\?", "?", text) #последовательности !?
        text = re.sub(r"[_]{2,}"," ", text) #последовательности ___ 
        text = re.sub(r"[…]+"," ", text) #последовательности …
        text = re.sub(r"[=]+"," ", text) #последовательности =


    #если перед или после ? идет знак препинания  -> оставляем только  ?
        text = re.sub(r"(\?[,!:;.])", "?", text) 
        text = re.sub(r"([,!:;.]\?)", "?", text)

    #если идут подряд всякие знаки, то оставляем один (первый из последовательности)
        def dashrepl2(matchobj):
            return matchobj.group()[0]
        text = re.sub(r"([,!:;.]+)", dashrepl2, text) 
    
        return text


    def change_spaces(self, text):
        """
        Заменим все пробельные символы на обычные пробелы (в них входят символы табуляции),
        при этом ставим условие, чтобы любой пробельный символ не повторялся более одного раза
        """
        return re.sub(r"\s+", " ", text)


    def clean_period_seq(self, s):
        """
        Чистим сообщения, которые состоят из одного уникального знака
        В частности, случаи ".", ". .", ". . .", ...
        """
        if type(s)==str:
            li = np.unique(s.split(' '))

            if len(li)==1 and len(li[0])==1:
                return ''
            elif len(li)==2 and 'от' in li and len(''.join(li))==3: 
                return ''
#                 if li[0]=='.':
#                     return ''
        return s
    
    
    def strip(self, text):
        return text.strip()

    # новая версия 
    def replace_names(self, text):
        """Удаляем имена вида: Иван Иван Иванович, И.И. Иванов, Иванов И.В."""
        return re.sub(r"([А-Я][а-я]+\s[А-Я](\.)[А-Я]\.)|([А-Я](\.)[А-Я]\.\s([А-Я]([а-я]+)))|([А-Я](\.|[а-я]+|)\s([А-Я](\.|[а-я]+))\s([А-Я]((\.|[а-я]+))))", " #ФИО# ", text)

    def lowering(self, text):
        return text.lower()

    def delete_pp(self, text):
        text = re.sub(r"p/p.", '', text)
        return text


    def delete_links(self, text):
        text = re.sub(r'https*\S+', ' #ссылка# ', text)
        text = re.sub(r'http*\S+', ' #ссылка# ', text)
        text = re.sub(r'www.*\S+', ' #ссылка# ', text)
        return text


    def remove_emails(self, text):
        text = re.sub(r'[\w\.-]+@[((A-Z)|(a-z)|(0-9))\.-]+', " #email# ", text)
        return text


    def delete_dates(self, text):
        
        self.DAYS_OF_WEEK = list(map(self.lowering, self.DAYS_OF_WEEK))
        self.MONTHS = list(map(self.lowering, self.MONTHS))

        #Если прям перед/после даты стоит ?, то чтобы его не потерять, оставляем его. В противном случае - пробел
        def dashrepl3(matchobj):
            if matchobj.group()[-1]=='?' or matchobj.group()[0]=='?':
                return '?'
            elif matchobj.group()[0]=='.':
                return '.'
            elif matchobj.group()[0]=='!':
                return '!'
            else:
                return ''
        #Ищем последовательности, чтобы перед(и после) даты был любой символ кроме буквы (или начало/конец строки)
        for day in self.DAYS_OF_WEEK:
            rx = r'([^a-zа-я]|^){0}($|[^a-zа-я])'.format(day)
            text = re.sub(rx, dashrepl3, text)

        for mon in self.MONTHS:
            rx = r'([^a-zа-я]|^){0}($|[^a-zа-я])'.format(mon)
            text = re.sub(rx, dashrepl3, text)

        #То же самое для года
        years = ["г.", "года", "год", "г"]

        for year in years:
            rx = r'([^a-zа-я]|^){0}($|[^a-zа-я])'.format(year)
            text = re.sub(rx, dashrepl3, text)
        return text