# classes.py
# This module connects front-end and back-end functionallity
# Functions call and write to the Model class that contains back-end functionlity

from model import Model
import pandas as pd
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
import os


class Funcs(QtWidgets.QWidget):

    def __init__(self):
        # Initialising the super class
        super(Funcs, self).__init__()
        # Different extensions of excel file uploaded
        self.filter_file = "Excel Files(*.csv *.xlsx *.xlsb)"
        # self.model is an instance of Model Class
        self.model = Model()
        # Initialising the lp_init
        self.lp_init()
        # Initialising the data Quality module
        self.dq_module_user_responses_default={'dqm_blank_cells_cbox': False,
                                               'dqm_fnctnl_trnx_amt_cbox': False,
                                               'dqm_error_thrshld_sbox': 0.0}
        ### Scenario Module
        self.sm_sc0_init()
        self.sm_sc2_init()
        self.sm_sc1_init()

        self.scenario_module_4_user_responses_default={
                                                       'sm_sc4_min_trnx_amt_thld_ledit': '',
                                                       'sm_sc4_ref_date_cbox': False,
                                                       'sm_sc4_flagged_trans_cbox': False,
                                                       'sm_sc4_ref_dt_dateEdit': '31/12/1999',
                                                       'sm_sc4_lk_bck_prd_ledit': '',
                                                       'sm_sc4_cum_trnx_amt_thld_ledit': '',
                                                       'sm_sc4_min_range_sbox': 0.0,
                                                       'sm_sc4_max_range_sbox': 0.0,
                                                        'sm_sc4_flagged_trans_cbox':False}
        self.scenario_module_3_user_responses_default={

                                                      'sm_sc3_min_trnx_amt_thld_cbox': False,
                                                      'sm_sc3_min_trnx_amt_thld_ledit': '',
                                                      'sm_sc3_ref_date_cbox': False,
                                                      'sm_sc3_ref_dt_dateEdit': '31/12/1999',
                                                      'sm_sc3_lk_bck_prd_ledit': '',
                                                      'sm_sc3_cum_trnx_amt_thld_ledit': '',
                                                      'sm_sc3_min_range_sbox': 0.0,
                                                      'sm_sc3_max_range_sbox': 0.0}

    def reset_backend_init(self):
        '''This method reinitialises all the backend classes in the same session'''

        # Scenario class
        self.model.scenarios_m.scenario_init()
        # Statistical Analysis Module
        self.model.statistical_analysis_m.stats_init()
        # DataFile upload Module
        self.model.data_extractor_m.DataFileUpload_reset()
        # Data quality module
        self.model.data_quality_m.DataQuality_reset()
        # Visualisation module
        self.model.viz_m.visualisation_init()

    def error_handling(self, error_log,success_msg):
        #print(error_log, success_msg)
        if success_msg is True:
            QMessageBox.about(self, "Success!!", 'Success')
        else:
            error_string = ''
            for key, value in error_log.items():
                if value:
                    error_string = str(error_string) + os.linesep + str(value) + "-" + str(key)
            #print("Error String:",error_string)
            QMessageBox.about(self, "Error Occured!!", error_string)


    def error_handling_dq_module(self,user_input_dict):
        #print("This is my latest Dict:", user_input_dict)
        '''This method takes the updated user input dictionary from data quality module and checks for error handling'''
        # dq_module_user_responses_default - default dictionary
        # Error is thrown for following reasons
            # if no user input is given, hence leaving dqm in default state
        if user_input_dict == self.dq_module_user_responses_default:
            self.throw_exception("You have not entered any input to perform the analysis ")
            # if check box is not checked
        elif user_input_dict['dqm_blank_cells_cbox'] == self.dq_module_user_responses_default['dqm_blank_cells_cbox']:
            self.throw_exception("Please select the data quality module check-box to proceed")
            # if error threshold is not changed given that functional transx amount box is checkec
        elif user_input_dict['dqm_fnctnl_trnx_amt_cbox'] == True and \
                user_input_dict['dqm_error_thrshld_sbox'] == self.dq_module_user_responses_default['dqm_error_thrshld_sbox']:
            self.throw_exception("Please enter the error threshold for funtional transaction analysis.")

        else:
            # if there is no error from the front end then below function is run
            '''
             Arguments: 1. latest transaction data
                        2. latest foreign exchange file
                        3. user given latest dictionary
            '''

            self.model.run_data_quality_module( self.model.data_extractor_m.tx_df, self.model.data_extractor_m.fx_df, user_input_dict)
            QMessageBox.about(self, "Success!!", "Analysis completed successfully")

    def error_handling_scenario3(self, user_input_dict):
        #print("This is my latest Dict:", user_input_dict)
        ''' This method takes the updated user input dictionary from scenario3 module and checks for error handling '''
        # scenario_module_3_user_responses_default - default dictionary
        # Error is thrown for following reasons
        # if no user input is given, hence leaving scenario3 in default state
        if user_input_dict == self.scenario_module_3_user_responses_default:
            self.throw_exception("You have not entered any input to perform the analysis ")
        elif user_input_dict['sm_sc3_cum_trnx_amt_thld_ledit'] == self.scenario_module_3_user_responses_default['sm_sc3_cum_trnx_amt_thld_ledit']:
            self.throw_exception("Please enter the cumulative large transaction threshold")

        elif(user_input_dict['sm_sc3_lk_bck_prd_ledit'] ==  self.scenario_module_3_user_responses_default[ 'sm_sc3_lk_bck_prd_ledit']):
            self.throw_exception('Enter the correct look back period')

        elif user_input_dict['sm_sc3_min_trnx_amt_thld_cbox'] == True and \
             user_input_dict['sm_sc3_min_trnx_amt_thld_ledit'] == self.scenario_module_3_user_responses_default['sm_sc3_min_trnx_amt_thld_ledit']:
            self.throw_exception("Please enter the filtering criteria (specify minimum transaction amount threshold)")

        elif(user_input_dict['sm_sc3_ref_date_cbox'] == True and user_input_dict['sm_sc3_ref_dt_dateEdit'] == self.scenario_module_3_user_responses_default['sm_sc3_ref_dt_dateEdit']):
              self.throw_exception("Please enter the correct reference date")

        elif(user_input_dict['sm_sc3_min_range_sbox'] >= user_input_dict['sm_sc3_max_range_sbox']):
            self.throw_exception("Please enter the % of Incoming & Outgoing % range")

        elif((self.check_invalid_inputs(user_input_dict['sm_sc3_lk_bck_prd_ledit'])==False) or (self.check_invalid_inputs(user_input_dict['sm_sc3_min_trnx_amt_thld_ledit'])==False)):
            self.throw_exception('Please dont enter invalid inputs such as [e,-,.,etc]. Only numbers are allowed')

        else:
            # runs the back end script for scenario5
            self.model.run_scenario3_analysis(user_input_dict)
            QMessageBox.about(self, "Success!!", "Analysis completed successfully")

    def error_handling_scenario4(self, user_input_dict):
        #print("This is my latest Dict:", user_input_dict)
        ''' This method takes the updated user input dictionary from scenario3 module and checks for error handling '''
        # scenario_module_4_user_responses_default - default dictionary
        # Error is thrown for following reasons
        # if no user input is given, hence leaving scenario4 in default state
        if user_input_dict == self.scenario_module_4_user_responses_default:
           self.throw_exception( "You have not entered any input to perform the analysis ")

        elif user_input_dict['sm_sc4_min_trnx_amt_thld_ledit'] == self.scenario_module_4_user_responses_default['sm_sc4_min_trnx_amt_thld_ledit']:
            self.throw_exception("Please enter the filtering criteria (specify minimum transaction amount threshold)")

        elif user_input_dict['sm_sc4_cum_trnx_amt_thld_ledit'] == self.scenario_module_4_user_responses_default['sm_sc4_cum_trnx_amt_thld_ledit']:
            self.throw_exception("Please enter the cumulative large transaction threshold")

        elif (user_input_dict['sm_sc4_lk_bck_prd_ledit'] == self.scenario_module_4_user_responses_default['sm_sc4_lk_bck_prd_ledit']):
            self.throw_exception('Enter the correct look back period')

        elif ((user_input_dict['sm_sc4_ref_date_cbox'] == True) and (user_input_dict['sm_sc4_ref_dt_dateEdit'] == self.scenario_module_4_user_responses_default['sm_sc4_ref_dt_dateEdit'])):
            self.throw_exception("Please enter the correct reference date")

        elif (user_input_dict['sm_sc4_min_range_sbox'] >= user_input_dict['sm_sc4_max_range_sbox']):
            self.throw_exception("Please enter the % of Incoming & Outgoing % range")

        elif((self.check_invalid_inputs(user_input_dict['sm_sc4_lk_bck_prd_ledit'])==False) or
             (self.check_invalid_inputs(user_input_dict['sm_sc4_cum_trnx_amt_thld_ledit'])==False)or
             (self.check_invalid_inputs(user_input_dict['sm_sc4_min_trnx_amt_thld_ledit'])==False)):
              self.throw_exception('Please dont enter invalid inputs such as [e,-,.,etc]. Only numbers are allowed')

        else:
            # runs the back end script for scenario4
            self.model.run_scenario4_analysis(user_input_dict)
            QMessageBox.about(self, "Success!!", "Analysis completed successfully")

    def sa_module_response_execute(self,rb1 = False,
                                        rb2 = False,
                                        amount1 = None,
                                        amount2 = None,
                                        check_box = False):
        input_params = {'level_population':True,
                             'level_account':False,
                             'accounts':[],
                             'percentile_input':amount1,
                             'sd_thold':amount2,
                             'return_n_transactions':check_box}
        ### Doing Preliminary Data Quality checks


        if ((self.check_invalid_inputs(input_params['percentile_input'])) == False or (self.check_invalid_inputs(input_params['sd_thold'])) == False):
            self.throw_exception('Please dont enter invalid inputs such as [e,-,.,etc]. Only numbers are allowed')

        else:
            self.model.run_statistical_analysis(input_params=input_params)
            self.error_handling(dict(enumerate(self.model.statistical_analysis_m.stats_module_issue_list)),
                    self.model.statistical_analysis_m.success_msg_sa)

    def sa_module_summary_button_execute(self,rb1,rb2,rb3):
        input_params = {'percentile_level':rb1,
                        'sd_level':rb2,
                        'transaction_level':rb3}
        #print(self.model.statistical_analysis_m.output_type)
        if self.model.statistical_analysis_m.success_msg_sa == False:
            self.throw_exception('Run Statistical Analysis First')

        elif (input_params['transaction_level'] and
        'monthly' not in self.model.statistical_analysis_m.output_type):
            self.throw_exception('Run Monthly Analysis First')
        elif (input_params['percentile_level'] and
        'percentile' not in self.model.statistical_analysis_m.output_type):
            self.throw_exception('Run Percentile Analysis First')
        elif (input_params['sd_level'] and
        'sd' not in self.model.statistical_analysis_m.output_type):
            self.throw_exception('Run SD Analysis First')
        else:
            try:
                result = self.model.statistical_analysis_m.export_summary(input_params)
            except:
                self.throw_exception('Error Creating Summary')
                result = 'Error Occurred'
            #print(result)
            return result

    def sa_module_generate_output(self):
        outputs = list(set(self.model.statistical_analysis_m.output_type))
        output_dict = {}
        for output_type in outputs:
            if output_type == 'sd':
                for k,v in self.model.statistical_analysis_m.output_sd.items():
                    output_dict['SD Analysis_'+k.split('_')[1].upper()] = v
            if output_type == 'monthly':
                for k,v in self.model.statistical_analysis_m.output_monthly.items():
                    output_dict['Montly Count Analysis_'+k.split('_')[1].upper()] = v
            if output_type == 'percentile':
                for k,v in self.model.statistical_analysis_m.output_percentile.items():
                    output_dict['Percentile Analysis_'+k.split('_')[1].upper()] = v
        return output_dict

    def write_excel(self, result = {}):
        '''This method exports the excel made from the dictionary of dataframes with key values as sheet names'''
        #if result is of None type
        if result is None:
            QMessageBox.about(self, "Warning!", "No file to export.")
        # if result dictionary is empty
        elif(result == {}):
            QMessageBox.about(self, "Warning!", "No file to export.")

        # opens the file dialog for the user to export the excel file
        else:
            save_path = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "C:/Users", filter="xlsx(*.xlsx)")
            if save_path[0] != '':
                writer = pd.ExcelWriter(save_path[0], engine = 'xlsxwriter')
                for key, value in result.items():
                    value.to_excel(writer, sheet_name = key,index = False)
                writer.save()


    def write_image(self, image = None):
        ''' This method exports the image for visualisation module'''
        if image is None:
            QMessageBox.about(self, "Warning!", "No image to export.")
        elif image == {}:
            QMessageBox.about(self, "Warning!", "No image to export.")
        else:
            save_path = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "C:/Users", filter="png(*.png)")
            if save_path[0] != '':
                image.savefig(save_path[0], bbox_inches = 'tight')

    ### Sanctioned countries Module
    def run_button_sc_module(self, account_level = False, percent = 10):
        input_params = {'Account Level Aggregation':account_level,
                        'Percentage':percent}
        if not(self.model.data_quality_m.success_msg_dqm):
            self.throw_exception('Run Data Quality Module First')
        #### can put other prelim checks elif
        else:
            try:
                self.model.run_sc_module(input_params)
            except:
                self.throw_exception('Error Calling Data Model')
        return

    ### Scenario Module

    def sm_sc_export_op(self, scenario):
        '''This method calls the outout from backend scripts and stores in result variable
         Arguments: s0 - for storing the scenario0 output in the result variable
                    s1 - for storing the scenario1 output in the result variable
                    s2 - for storing the scenario2 output in the result variable
                    s3 - for storing the scenario3 output in the result variable
                    s4 - for storing the scenario4 output in the result variable
        '''
        if (scenario == 's0'):
            result = self.model.scenarios_m.sc0_exports_dict

        elif(scenario=='s1'):
            result = self.model.scenarios_m.sc1_exports_dict

        elif(scenario=='s2'):
            result = self.model.scenarios_m.sc2_exports_dict

        elif(scenario=='s3'):
            result = self.model.scenarios_m.sc3_exports_dict

        elif(scenario=='s4'):
            result = self.model.scenarios_m.sc4_exports_dict

        # Result is dictonary of dataframes and goes as an arguments in write_excel function
        self.write_excel(result)

    def upload_btn(self, key):
        ''' This method helps in storing the path of the file (single or multiple) given by user '''
        # Opens the dialog box and key value is stored in respective dictionary
        open_path = QtWidgets.QFileDialog.getOpenFileNames(self, "Open File", "C:/Users",  filter="Excel Files(*.csv *.xlsx *.xlsb)")
        # upload single file
        # if single file is uploaded
        # checking the length of number of files uploaded
        if (len(open_path[0]) == 1):
            # storing the path of account number file for scenario1
            if(key=='sm_sc1_upload_act_nums_btn'):
                self.sm_sc1_input_dict[key] = open_path[0][0]
            # storing the path of account number file for scenario0
            elif (key == 'sm_sc0_upload_act_nums_btn'):
                self.sm_sc0_input_dict[key] = open_path[0][0]
            # storing the path of account number file for scenario2
            elif(key=='sm_sc2_upload_act_nums_btn'):
                self.sm_sc2_input_dict[key] = open_path[0][0]
            # storing the path of high risk, sanctioned, exchange rate, swift files
            elif (key == 'lp_hrc_btn' or key=='lp_sc_btn' or key=='lp_fx_btn' or key=='lp_full_swft_files_btn' or key=='lp_txn_files_btn' or key =='lp_in_swft_files_btn' or key =='lp_out_swft_files_btn'):
                self.lp_input_dict[key] = open_path[0][0]

        # upload multiple files
        # checking the length of number of files uploaded
        elif(len(open_path[0]) > 1):
            # storing the path of transaction files and swift files
            if(key=='lp_txn_files_btn' or key=='lp_full_swft_files_btn' or key =='lp_in_swft_files_btn' or key=='lp_out_swft_files_btn' ):
                self.lp_input_dict[key] = open_path[0][0:len(open_path[0])]
            else:
                self.throw_exception('Only single file is allowed')
        else:
            pass

    def throw_exception(self, error):
        ''' Dialog box customisation'''
        box = QMessageBox()
        box.setIcon(QMessageBox.Critical)
        box.setWindowTitle('Error')
        box.setText(error)
        box.setStandardButtons(QMessageBox.Ok)
        box.exec()

    def sm_sc0_init(self):
        # scenario_module_0_user_responses_default - default dictionary having default values for scenario0
        self.scenario_module_0_user_responses_default = {'sm_sc0_popltn_rbtn': True,
                                                         'sm_sc0_account_rbtn': False,
                                                         'sm_sc0_upload_act_nums_btn':''}

        # dictionary contains the most recent user inputs from the front end
        self.sm_sc0_input_dict = {}
        self.sm_sc0_input_dict['sm_sc0_upload_act_nums_btn'] = self.scenario_module_0_user_responses_default['sm_sc0_upload_act_nums_btn']

    def sm_sc0_error_handling(self):
        ''' Checking the error handing from the front end and after passing all the checks sends the updated dictionary
            Error is thrown: 1. if user doesn't input minimum transaction threshold
                             2. if account file is not uploaded given that account radio button is clickec
        '''
        if (self.sm_sc0_input_dict['sm_sc0_min_trnx_amt_thld_ledit'] == ''):
            self.throw_exception('Enter the minimum threshold transaction amount')

        elif (self.sm_sc0_input_dict['sm_sc0_account_rbtn'] == True and self.sm_sc0_input_dict[
            'sm_sc0_upload_act_nums_btn'] == ''):
            self.throw_exception('Please upload the file')

        elif(self.check_invalid_inputs(self.sm_sc0_input_dict['sm_sc0_min_trnx_amt_thld_ledit'])==False):
            self.throw_exception('Please dont enter invalid inputs such as [e,-,.,etc]. Only numbers are allowed')

        else:
                # runs the back end script for scenario0
            self.model.scenario_zero(self.sm_sc0_input_dict.copy())
            QMessageBox.about(self, "Success!!", "Analysis completed successfully")

    def sm_sc1_init(self):
        # scenario_module_1_user_responses_default - default dictionary having default values for scenario1
        self.scenario_module_1_user_responses_default = {'sm_sc1_popltn_rbtn': True,
                                                         'sm_sc1_account_rbtn': False,
                                                         'sm_sc1_min_trnx_amt_thld_ledit': '',
                                                         'sm_sc1_incum_trnx_amt_thld_ledit':'',
                                                         'sm_sc1_outcum_trnx_amt_thld_ledit':'',
                                                         'sm_sc1_inoutcum_trnx_amt_thld_ledit':'',
                                                         'sm_sc1_ref_dt_dateEdit': '31/12/1999',
                                                         'sm_sc1_ref_date_cbox': False,
                                                         'sm_sc1_lk_bck_prd_ledit': '',
                                                         'sm_sc1_upload_act_nums_btn': ''
                                                           }

        # dictionary contains the most recent user inputs from the front end
        self.sm_sc1_input_dict = {}
        self.sm_sc1_input_dict['sm_sc1_upload_act_nums_btn'] = self.scenario_module_1_user_responses_default['sm_sc1_upload_act_nums_btn']

    def sm_sc1_error_handling(self):
        ''' Checking the error handing from the front end and after passing all the checks sends the updated dictionary
            Error is thrown: 1. if user doesn't input minimum transaction threshold
                             2. if user doesn't input look back period
                             3. if user doesn't upload account number file after checking the account number radio button
                             4. if user doesn't input all the thresholds
                             5. if user doesn't reference date after clicking on the raference date checkbox
        '''
        if(self.sm_sc1_input_dict['sm_sc1_min_trnx_amt_thld_ledit'] == ''):
            self.throw_exception('Enter the minimum threshold transaction amount')

        elif(self.sm_sc1_input_dict['sm_sc1_lk_bck_prd_ledit']==''):
            self.throw_exception('Enter the look back period')

        elif(self.sm_sc1_input_dict['sm_sc1_account_rbtn'] == True and self.sm_sc1_input_dict['sm_sc1_upload_act_nums_btn'] == ''):
            self.throw_exception('Please upload the file')

        elif(self.sm_sc1_input_dict['sm_sc1_incum_trnx_amt_thld_ledit']=='' or self.sm_sc1_input_dict['sm_sc1_outcum_trnx_amt_thld_ledit']=='' or self.sm_sc1_input_dict['sm_sc1_inoutcum_trnx_amt_thld_ledit']==''):
            self.throw_exception('Fill all the threshold transaction amount')

        elif((self.sm_sc1_input_dict['sm_sc1_ref_date_cbox'] == True) and self.sm_sc1_input_dict['sm_sc1_ref_dt_dateEdit'] == '31/12/1999'):
            self.throw_exception('Enter the reference date')

        elif((self.check_invalid_inputs(self.sm_sc1_input_dict['sm_sc1_min_trnx_amt_thld_ledit'])==False) or
             (self.check_invalid_inputs(self.sm_sc1_input_dict['sm_sc1_incum_trnx_amt_thld_ledit']) == False) or
             (self.check_invalid_inputs(self.sm_sc1_input_dict['sm_sc1_outcum_trnx_amt_thld_ledit']) == False) or
             (self.check_invalid_inputs(self.sm_sc1_input_dict['sm_sc1_inoutcum_trnx_amt_thld_ledit']) == False)):
             self.throw_exception('Please dont enter invalid inputs such as [e,-,.,etc]. Only numbers are allowed')

        else:
            #print(self.sm_sc1_input_dict)
            # runs the back end script for scenario1
            self.model.scenario_one(self.sm_sc1_input_dict.copy())
            QMessageBox.about(self, "Success!!", "Analysis completed successfully")

    def sm_sc2_init(self):
        # scenario_module_2_user_responses_default - default dictionary having default values for scenario2
        self.scenario_module_2_user_responses_default = {'sm_sc2_popltn_rbtn': False,
                                                         'sm_sc2_account_rbtn': False,
                                                         'sm_sc2_upload_act_nums_btn': '',
                                                         'sm_sc2_min_trnx_amt_thld_cbox': False,
                                                         'sm_sc2_min_trnx_amt_thld_ledit': '',
                                                         'sm_sc2_ref_date_cbox': False,
                                                         'sm_sc2_ref_dt_dateEdit': '31/12/1999',
                                                         'sm_sc2_lk_bck_prd_ledit': '',
                                                         'sm_sc2_instd_dev_ledit': '',
                                                         'sm_sc2_outstd_dev_ledit': '',
                                                         'sm_sc2_inoutstd_dev_ledit':'',
                                                         'sm_sc2_thld_in_ledit':'',
                                                         'sm_sc2_thld_out_ledit':'',
                                                         'sm_sc2_thld_in_out_ledit':''
                                                         }
        # dictionary contains the most recent user inputs from the front end
        self.sm_sc2_input_dict = {}
        self.sm_sc2_input_dict['sm_sc2_upload_act_nums_btn'] = self.scenario_module_2_user_responses_default['sm_sc2_upload_act_nums_btn']

    def sm_sc2_error_handling(self):
        ''' Checking the error handing from the front end and after passing all the checks sends the updated dictionary
              Error is thrown: 1. if user doesn't input minimum transaction threshold
                               2. if user doesn't input look back period
                               3. if user doesn't upload account number file after checking the account number radio button
                               4. if user doesn't input all the thresholds and standard deviation
                               5. if user doesn't reference date after clicking on the raference date checkbox
        '''
        if(self.sm_sc2_input_dict['sm_sc2_min_trnx_amt_thld_cbox'] == True and
              self.sm_sc2_input_dict['sm_sc2_min_trnx_amt_thld_ledit'] == ''):
                self.throw_exception('Enter the minimum threshold transaction')

        elif (self.sm_sc2_input_dict['sm_sc2_instd_dev_ledit'] == '' or self.sm_sc2_input_dict['sm_sc2_outstd_dev_ledit'] == ''
            or self.sm_sc2_input_dict['sm_sc2_inoutstd_dev_ledit'] == '' or self.sm_sc2_input_dict['sm_sc2_thld_in_ledit'] == ''
            or self.sm_sc2_input_dict['sm_sc2_thld_out_ledit'] == '' or self.sm_sc2_input_dict[ 'sm_sc2_thld_in_out_ledit'] == ''):
            self.throw_exception('Please enter all the standard deviation and thresholds')

        elif(self.sm_sc2_input_dict['sm_sc2_lk_bck_prd_ledit']==''):
            self.throw_exception('Please enter the look back period')

        elif (self.sm_sc2_input_dict['sm_sc2_ref_date_cbox'] == True and self.sm_sc2_input_dict['sm_sc2_ref_dt_dateEdit'] == '31/12/1999'):
            self.throw_exception('Enter the reference date')

        elif (self.sm_sc2_input_dict['sm_sc2_account_rbtn'] == True and self.sm_sc2_input_dict[
            'sm_sc2_upload_act_nums_btn'] == ''):
            self.throw_exception('Upload the input file')

        elif((self.check_invalid_inputs(self.sm_sc2_input_dict['sm_sc2_min_trnx_amt_thld_ledit'])==False) or
             (self.check_invalid_inputs(self.sm_sc2_input_dict['sm_sc2_lk_bck_prd_ledit'])==False) or
             (self.check_invalid_inputs(self.sm_sc2_input_dict['sm_sc2_instd_dev_ledit']) == False) or
             (self.check_invalid_inputs(self.sm_sc2_input_dict['sm_sc2_outstd_dev_ledit']) == False) or
             (self.check_invalid_inputs(self.sm_sc2_input_dict['sm_sc2_inoutstd_dev_ledit'])== False) or
             (self.check_invalid_inputs(self.sm_sc2_input_dict['sm_sc2_thld_in_ledit'])== False) or
             (self.check_invalid_inputs(self.sm_sc2_input_dict['sm_sc2_thld_out_ledit']) == False) or
             (self.check_invalid_inputs(self.sm_sc2_input_dict['sm_sc2_thld_in_out_ledit'])== False)):

            self.throw_exception('Please dont enter invalid inputs such as [e,-,.,etc]. Only numbers are allowed')

        else:
            #print(self.sm_sc2_input_dict)
            # runs the back end script for scenario2
            self.model.scenario_two(self.sm_sc2_input_dict.copy())
            QMessageBox.about(self, "Success!!", "Analysis completed successfully")


    def lp_init(self):
        # lp_input_dict - default dictionary having default values for scenario2
        self.lp_input_dict = { 'lp_txn_files_btn': '',
                                                         'lp_fx_btn': '',
                                                         'lp_hrc_btn': '',
                                                         'lp_sc_btn': '',
                                                         'lp_full_swft_files_btn': ''
                                                        ,'lp_in_out_swift_cbox': False,
                                                          'lp_full_swift_cbox': False,
                                                        'lp_in_swft_files_btn':'',
                                                        'lp_out_swft_files_btn':'',
                                                        'lp_bic_code_ledit':''
                                                        }
    def lp_error_handling(self):
        ''' Checking the error handing from the front end and after passing all the checks sends the updated dictionary
              Error is thrown: 1. if neither transaction file not swift file is uploaded
                               2. If BIC code is not present given that swift file is uploaded
                               3. if foreign exchange rate file is not uploaded given that swift file is uploaded
                               4.
        '''
        if (self.lp_input_dict['lp_txn_files_btn'] == '' and self.lp_input_dict['lp_in_swft_files_btn'] == '' and self.lp_input_dict['lp_out_swft_files_btn'] == '' and self.lp_input_dict[
                    'lp_full_swft_files_btn'] == ''):
            self.throw_exception('Please upload transaction files or swift files')

        elif(self.lp_input_dict['lp_full_swift_cbox']==True and (self.lp_input_dict['lp_full_swft_files_btn']=='' or self.lp_input_dict['lp_bic_code_ledit']=='')):
                self.throw_exception('Please enter the BIC code and upload the  swift files')

        elif( self.lp_input_dict['lp_in_swft_files_btn']=='' and self.lp_input_dict['lp_in_out_swift_cbox'] ==True and self.lp_input_dict['lp_out_swft_files_btn']==''):
            self.throw_exception('Please upload the swift file')

        elif ((self.lp_input_dict['lp_full_swift_cbox']==True or self.lp_input_dict['lp_in_out_swift_cbox'] ==True) and self.lp_input_dict['lp_fx_btn']==''):
            self.throw_exception('Please upload the exchange rate file')

        else:
            new_dict = self.convert_dict_list(self.lp_input_dict.copy())
            #print(new_dict)
            # runs the backend scripts of landing page by sending updated dictionary
            self.model.lp_send_dict(new_dict)

    def convert_dict_list(self, dict):
        #This method converts the values in the dictionary into the list '''
       for key in dict.keys():
           if(type(dict[key])!=type([])):
               dict[key]=[dict[key]]
       return dict

    def lp_upload_file(self):
        self.model.lp_upload_btn()

    def lp_export_swift_file(self):
        # This method is used to export the processed swift data on landing page
        dict ={}
        # swift_df is the dataframe - contains the latest processed swift data
        df = self.model.data_extractor_m.swift_df
        if(df is None):
            QMessageBox.about(self, "Warning!", "No file to export.")
        else:
            dict = {'Swift File': df}
            #print(df)
            self.write_excel(dict)

    ##############VisualizaTION mODEULE

    def throw_warning(self, error):
        # Message box customisation to throw error/warning
        box = QMessageBox()
        box.setWindowTitle('Warning')
        box.setText(error)
        box.setStandardButtons(QMessageBox.Ok)
        box.exec()

    def viz_module_response_execute(self, amount_box=False,
                                    amount1=False,
                                    date1=None,
                                    date2=None):
        '''This method takes the input from the front end visualisation module
        arguments: 1. amount_box -> check box for enabling transaction threshold
                   2. amount1 -> transaction threshold
                   3. date1 -> start date
                   4. date2 -> end date
        '''
        # converting date1 and date2 into dataframe
        try:
            date1 = pd.to_datetime(date1, dayfirst=True)
            date2 = pd.to_datetime(date2, dayfirst=True)
        except:
            self.throw_exception('Inavlid Data Provided')
        input_params = {'Amount_filter_flag': amount_box,
                        'Amount': amount1,
                        'Start Date': date1,  # pd.datetime
                        'End Date': date2  # pd.datetime
                        }
        # error is thrown if data quality module hasn't been run

        if((self.check_invalid_inputs(input_params['Amount']))==False):
            self.throw_exception('Please dont enter invalid inputs such as [e,-,.,etc]. Only numbers are allowed')
        else:
            error_not_displayed = True
            try:
                #run visualisation module at the backend
                #arguments: input_params is dictionary of user input
                self.model.run_visualisation(input_params)
            except:
                self.throw_exception('Error Occured')
                self.error_handling(self.model.viz_m.error_log, False)
                error_not_displayed = False
            if error_not_displayed:
                if any(value is not None for value in self.model.viz_m.error_log.values()):
                    err_text = '\n'.join(
                        [str(value) for value in self.model.viz_m.error_log.values() if value is not None])
                    self.throw_warning(err_text)

        return

    def upload_btn_viz(self):
        '''This method checks the number of files selected by the user'''
        open_path = QtWidgets.QFileDialog.getOpenFileNames(self, "Open File", "C:/Users",    filter="Excel Files(*.csv *.xlsx *.xlsb)")
        # upload single file
        if (len(open_path[0]) == 1):
            return open_path[0]
        # upload multiple files
        elif(len(open_path[0]) > 1):
            self.throw_exception('Only single file is allowed')
        else:
            pass


## sanctioned countries

    def sanctioned_ctry_run(self):
        #runs the backend sanctioned countries module
        self.model.sanctioned_ctry_mod_run()
        QMessageBox.about(self, "Success!!", "Analysis completed successfully")


    def SHRC_export_file(self):
        # stores the output in the dict call the function to write it into excel
        dict = self.model.sanctioned_countries_m.exports_dict
        self.write_excel(dict)


    def check_invalid_inputs(self,value):
        chars = set('e.-,')
        if any((c in chars) for c in value):
            return False
        else:
            return True

