import numpy as np

from UtilsCleaning import Utilities


class CleanText(Utilities):
    """
    Class that takes list of texts
    Inherits Utilities class which contains functions for different steps of cleaning

    Params:
    -------

    list of texts: list

    Methods:
    -------

    clean(instance attr): -> cleans every text in a list
    """
    def clean(self, list_of_texts: list) -> list:
        """
        Perform cleaning of list of texts with functions from UTILITIES class in appropriate order.
        
        Return:
        --------
          list with cleaned texts
        """
        cleaned_list = []
        for text in list_of_texts:
            #print(text, '\n\n')
            text = str(text)
            text = self.delete_support_message(text)
            print(f'After delete_support_message:   {text}')
            text = self.html_remover(text)
            print(f'After html_remover:   {text}')
            text = self.delete_end_of_message(text)
            print(f'After delete_end_of_message:   {text}')
            text = self.add_period(text)
            print(f'After add_period:   {text}')
            text = self.change_spaces(text)
            print(f'After change_spaces:   {text}')
            text = self.replace_account_numbers(text)
            print(f'After replace_account_numbers:   {text}')
            text = self.replace_phone_numbers(text)
            print(f'After replace_phone_numbers:   {text}')
            text = self.remove_emails(text)
            print(f'After remove_emails:   {text}')
            text = self.delete_numbers_with_prep(text)
            print(f'After delete_numbers_with_prep:   {text}')
            text = self.delete_extra_puctuation(text)
            print(f'After delete_extra_puctuation:   {text}')
            text = self.change_spaces(text)
            print(f'After change_spaces:   {text}')
            text = self.strip(text)
            print(f'After strip:   {text}')
            #text = self.clean_period_seq(text)
            #print(f'After clean_text:   {text}')
            text = self.replace_names(text)
            print(f'After delete_names:   {text}')
            text = self.lowering(text)
            print(f'After lowering:   {text}')
            text = self.delete_pp(text)
            print(f'After delete_pp:   {text}')
            text = self.delete_links(text)
            print(f'After delete_links:   {text}')
            text = self.delete_dates(text)
            print(f'After delete_dates:   {text}')
            text = self.change_spaces(text)
            print(f'After change_spaces:   {text}') 
            text = self.delete_extra_puctuation(text)
            print(f'After delete_extra_puctuation:   {text}')
            text = text.strip()
            print(f'After strip:   {text}')
            text = self.clean_period_seq(text)
            print(f'After clean_period_seq:   {text}')
            print(f'FINAL:   {text}')

            cleaned_list.append(text)

        # print(cleaned_list)
        return cleaned_list