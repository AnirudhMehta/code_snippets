# ui_modules.py
# This file connects signals(buttons) UI from and slots(functions) Backend
# Main Functionality is stored in classes.py(Funcs class)
# UI design elements are located in Front_End_Design.py(converted from UI file)

from UI import Front_End_Design
from classes import Funcs
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QDoubleValidator, QIntValidator
import os, shutil

class Ui_MainWindow_with_Funcs(Front_End_Design.Ui_MainWindow):

    '''
    Description of Ui_MainWindow_with_Funcs class
    Ui_MainWindow_with_Funcs ->
        1. can access the methods and attributes defined in the super class 'Front_End_Design.Ui_MainWindow'
        2. can initialise all the methods defined in funcs class defined in classes.py

        # attributes: refers to all the tabs name, widgets name, positions and respective information.
        Hence, all widgets available in GUI can be accesses here
        Example: self.<<object(widget) name>>
    '''
    ### Init with UI_MainWindow
    def __init__(self):

        ''' Initialise the init method of super class (Front_End_Design.Ui_Mainwindow) '''
        super().__init__()

        ''' Initialise the Funcs class'''
        self.funcs = Funcs()


    ### Setting up the UI
    def setupUi(self, MW):
        '''setting up the GUI window'''
        super().setupUi( MW )
        '''Initialising all the backend classes -> Landing page(lp), statistics analysis module(sam),
        data quality(dq), scenario module(sc), visualisation module(viz), Sanctioned countries module (scm), 
        '''

        self.lp_init()
        self.sa_module()
        self.dq_module()
        self.sm_sc_module_init()
        self.viz_module()
        self.sanctiond_ctry_init()

        '''disabla tabs - disable all the separate tab and module after creating a new session'''
        self.disabla_tabs()
        self.dqm_fnctnl_trnx_amt_cbox.setDisabled(True)

        '''Here Pickle file refers to concatenation of recent transaction and swift transaction data uploaded in
        the current session, stored in 'tms_app' directory in Users folder. This 'tms_app' directory is deleted automatically when 
        a new session is initialised'''

        self.del_pickle_file()

    def disabla_tabs(self):
        # data quality tab is being disabled
        self.dqm.setDisabled(True)
        # statistical analysis module tab is being disabled
        self.sam.setDisabled(True)
        #scenario module is being disabled
        self.sm.setDisabled(True)
        #sanctioned country module is being disabled
        self.sc.setDisabled(True)
        #visualisation is being disabled
        self.vis.setDisabled(True)

    ## Landing page
    def lp_init(self):
        '''This method has all clickable widgets with events triggered on respective clicks for landing page'''

        # click on reset button triggers the front end reset function
        self.lp_reset_btn.clicked.connect(self.front_end_reset)
        # click on reset button triggers the back end reset function
        self.lp_reset_btn.clicked.connect(self.funcs.reset_backend_init)
        # This method is activated. 'ctrl + click' on it for more information
        self.lp_upload_bt()
        # click on check schema button triggers the upload_files_landing_page
        self.lp_check_schma_btn.clicked.connect(self.upload_files_landing_page)
        # click on check schema button triggers the lp_error_handling
        self.lp_check_schma_btn.clicked.connect(self.funcs.lp_error_handling)
        # click on check schema button triggers the summary_button_check_lp_module
        self.lp_check_schma_btn.clicked.connect(self.summary_button_check_lp_module)
        # click on check schema button triggers the events_lp_check_schema
        self.lp_check_schma_btn.clicked.connect(self.events_lp_check_schema)
        # click on upload button triggers the lp_upload_file
        self.lp_upload_btn.clicked.connect(self.funcs.lp_upload_file)
        # click on upload button triggers the events_lp_run_btn
        self.lp_upload_btn.clicked.connect(self.events_lp_run_btn)
        # click on upload button triggers the summary_button_upload_lp_module
        self.lp_upload_btn.clicked.connect(self.summary_button_upload_lp_module)
        # click on reset button triggers the upload_reset
        self.lp_upload_btn.clicked.connect(self.upload_reset)

        # click on upload button triggers the lp_export_swift_file
        self.lp_export_swft_files_btn.clicked.connect(self.funcs.lp_export_swift_file)

    def events_lp_check_schema(self):
        # when ready_to_upload_allfiles becomes true then only upload button becomes enable otherwise will be disabled
        if (self.funcs.model.data_extractor_m.ready_to_upload_allfiles == True):
            # Landing page upload button is being enabled
            self.lp_upload_btn.setEnabled(True)

    def events_lp_run_btn(self):
        # if incorrect schema files are present or upload process is finished- Disable the upload button
        if (self.funcs.model.data_extractor_m.ready_to_upload_allfiles == False or self.funcs.model.data_extractor_m.check_file_status_sum == False):
            self.lp_upload_btn.setDisabled(True)

        # uploaded_compltn_status is a dictionary contains the boolean value for all the uploaded files
        # data quality module is enabled only if either transaction or swift files are uploaded
        if (self.funcs.model.data_extractor_m.uploaded_compltn_status.get('Transact File') == True or
                self.funcs.model.data_extractor_m.uploaded_compltn_status.get('Swift File') == True):
            self.dqm.setEnabled(True)
        # dqm_fnctnl_trnx_amt_cbox is enabled only if FX files are uploaded
        if (self.funcs.model.data_extractor_m.uploaded_compltn_status.get('FX File') == True):
            self.dqm_fnctnl_trnx_amt_cbox.setEnabled(True)


    def front_end_reset(self):
        # clears out the landing page summary
        self.lp_sum_txtbrow.clear()
        # clears out the data quality module summary
        self.dqm_summary_out_txt_brow.clear()
        # clears out the statistical analysis module summary
        self.sam_summary_out_txt_brow.clear()
        # clears out the visualisation tab summary
        self.vis_smpl_export_txt_brow.clear()
        # class the lp_init function from class
        self.funcs.lp_init()
        # calls the disabla tabs function
        self.disabla_tabs()
        self.dqm_fnctnl_trnx_amt_cbox.setDisabled(True)
        # calls the del pickle file function
        self.del_pickle_file()
        #Default state unticks the functional transaction box on reset
        self.dqm_fnctnl_trnx_amt_cbox.setChecked(False)

    def upload_reset(self):
        self.dqm_summary_out_txt_brow.clear()
        self.sam_summary_out_txt_brow.clear()
        self.vis_smpl_export_txt_brow.clear()
        self.disabla_tabs()
        # DQM table is enabled
        self.dqm.setEnabled(True)

    def summary_button_check_lp_module(self):
        '''This method updates the summary status of recent files for which scheme check has been done'''
        # Clears out the summary on landing page
        self.lp_sum_txtbrow.clear()
        # check_file_complete_status becomes true if schema check has been done
        if self.funcs.model.data_extractor_m.check_file_complete_status == True:
            # copying the check_file_status_sum_df in df
            df = self.funcs.model.data_extractor_m.check_file_status_sum_df
            # conversion of dataframe into html
            df1 = df.to_html(index=False, border=0.1)
            # displaying the converted html content on text browser
            self.lp_sum_txtbrow.setHtml(df1)

    def summary_button_upload_lp_module(self):
        '''This method updates the summary status of uploaded files after uploading process is finished'''
        # Clears out the landing page summary
        self.lp_sum_txtbrow.clear()
        # ready_to_upload_allfiles becomes false after the current uploading process is finished
        if self.funcs.model.data_extractor_m.ready_to_upload_allfiles == False:
            # Copying the summary output into data-frame
            df = self.funcs.model.data_extractor_m.check_file_status_sum_df
            # conversion of dataframe into html
            df1 = df.to_html(index=False, border=0.1)
            # displaying the converted html content on text browser
            self.lp_sum_txtbrow.setHtml(df1)

    def upload_files_landing_page(self):
        '''This method takes the user input from front end and updates the dictionary passed to backend'''
        # key = lp_in_out_swift_cbox (check box for uploading in and out swift files) and value is boolean
        self.funcs.lp_input_dict['lp_in_out_swift_cbox'] = self.lp_in_out_swift_cbox.isChecked()
        # key = lp_full_swift_cbox (check box for uploading full swift files) and value is boolean
        self.funcs.lp_input_dict['lp_full_swift_cbox'] = self.lp_full_swift_cbox.isChecked()
        # key = lp_bic_code_ledit (line edit for BIC code) and value is user input
        self.funcs.lp_input_dict['lp_bic_code_ledit'] = self.lp_bic_code_ledit.text()

    def lp_upload_bt(self):
        '''This method updates the landing page dictionary with updated path of different kinds of files '''
        # click on lp_in_swft_files_btn  triggers the upload_btn method in funcs class by passing the key
        self.lp_in_swft_files_btn.clicked.connect(lambda: self.funcs.upload_btn('lp_in_swft_files_btn'))
        # click on lp_out_swft_files_btn  triggers the upload_btn method in funcs class by passing the key
        self.lp_out_swft_files_btn.clicked.connect(lambda: self.funcs.upload_btn('lp_out_swft_files_btn'))
        # click on lp_full_swft_files_btn triggers the upload_btn method in funcs class by passing the key
        self.lp_full_swft_files_btn.clicked.connect(lambda: self.funcs.upload_btn('lp_full_swft_files_btn'))

        # click on lp_txn_files_btn (Transaction files) triggers the upload_btn method in funcs class by passing the key
        self.lp_txn_files_btn.clicked.connect(lambda: self.funcs.upload_btn('lp_txn_files_btn'))
        # click on lp_fx_btn(Foreign exchange file) triggers the upload_btn method in funcs class by passing the key
        self.lp_fx_btn.clicked.connect(lambda: self.funcs.upload_btn('lp_fx_btn'))
        # click on lp_hrc_btn(high risk files) triggers the upload_btn method in funcs class by passing the key
        self.lp_hrc_btn.clicked.connect(lambda: self.funcs.upload_btn('lp_hrc_btn'))
        # click on lp_sc_btn(sanctioned countries file) triggers the upload_btn method in funcs class by passing the key
        self.lp_sc_btn.clicked.connect(lambda: self.funcs.upload_btn('lp_sc_btn'))

    def dq_module(self):
        ''' This method has all the clickable widgets of data quality module and functions triggered with the click events '''
        # when run button is clicked in data quality module, it triggers the run_button_dq_module
        self.dqm_run_btn.clicked.connect(self.run_button_dq_module)
        # when run button is clicked in data quality module, it triggers the dqm_summary_response_catch
        self.dqm_run_btn.clicked.connect(self.dqm_summary_response_catch)
        # when data export button is clicked in data quality module, it triggers the export_button_dq_module
        self.dqm_dexport_btn.clicked.connect(self.export_button_dq_module)
        # when run button is clicked in data quality module, it triggers the events_dqm_run_btn
        self.dqm_run_btn.clicked.connect(self.events_dqm_run_btn)

    def events_dqm_run_btn(self):

        if (self.funcs.model.data_quality_m.success_msg_dqm == True and len(self.funcs.model.get_tx_df().index)!=0):
            self.sam.setEnabled(True)
            self.vis.setEnabled(True)

        if (self.funcs.model.data_quality_m.success_msg_dqm == True and
                self.funcs.model.data_extractor_m.uploaded_compltn_status.get('HRC File') == True and len(self.funcs.model.get_tx_df().index)!=0):
            self.sm.setEnabled(True)

        if (self.funcs.model.data_quality_m.success_msg_dqm == True and
                self.funcs.model.data_extractor_m.uploaded_compltn_status.get(
                    'SC File') == True and self.funcs.model.data_extractor_m.uploaded_compltn_status.get(
                    'HRC File') == True and len(self.funcs.model.get_tx_df().index)!=0):
            self.sc.setEnabled(True)

    def run_button_dq_module(self):
        ''' This function takes all the user input in dqm module and send it to error_handling_dq_module function in Funcs class
            Find the detailed description of arguments in the same order
        :argument - checkbox for blank cells
                  - checkbox for functional transaction amount
                  - checkbox for error threshold spin box - takes value > 0
        '''
        self.funcs.error_handling_dq_module({'dqm_blank_cells_cbox': self.dqm_blank_cells_cbox.isChecked(),
                                             'dqm_fnctnl_trnx_amt_cbox': self.dqm_fnctnl_trnx_amt_cbox.isChecked(),
                                             'dqm_error_thrshld_sbox': self.dqm_error_thrshld_sbox.value()})

    def export_button_dq_module(self):
        ''' This function is triggered(called) on click event of data export button in data quality module '''
        # This function takes the most updated result (exception data and clean data) from data quality module and send it to write_excel function in Funcs class for exporting
        self.funcs.write_excel(self.funcs.model.data_quality_m.output_dict_dqm)

    def dqm_summary_response_catch(self):
        ''' This function prints the summary of transaction data in dqm after the run button is clicked '''
        # Clears out the text browser widget
        self.dqm_summary_out_txt_brow.clear()

        # success_msg_dqm is true only after the back end processing of data quality module
        if self.funcs.model.data_quality_m.success_msg_dqm == True:
            # summary output is stored in data-frame
            df = self.funcs.model.data_quality_m.summary_output
            # Content in data-frame is converted into html content
            df1 = df.to_html(index=False, border=0.1)
            # setting the converted html content into text browser
            self.dqm_summary_out_txt_brow.setHtml(df1)


    ### Statistical Module

    def sa_module(self):

        ''' This method has all the click-able widgets of statistical analysis module and functions triggered with the click events '''

        # Setting the validator (only accepts double type values from the front end) for percentile threshold of functional transactional amounts
        self.sam_prcntl_func_trnx_amt_ledit.setValidator(QDoubleValidator()),
        # Setting the validator (only accepts double type values from the front end) for standard deviation threshold
        self.sam_std_dev_ledit.setValidator(QDoubleValidator()),
        # when run button is clicked in statistical analysis module, it triggers the run_button_sa_module
        self.sam_run_btn.clicked.connect(self.run_button_sa_module)
        # when data export button is clicked in statistical analysis module, it triggers the export_button_sa_module
        self.sam_dexport_btn.clicked.connect(self.export_button_sa_module)
        # when submit button is clicked in statistical analysis module, it triggers the summary_button_sa_module
        self.sam_submit_btn.clicked.connect(self.summary_button_sa_module)
        return

    def run_button_sa_module(self):
        ''' This method takes the user input from the front end and send it to sa_module_response_execute for processing
        Find the detailed description of arguments in the same order
        :argument - True is for radiobutton -> showing the summary of the result
                  - user input text for percentile threshold of functional transaction amounts
                  - user input text for standard deviation threshold
                  - user input boolean value for checkbox
          - checkbox for error threshold spin box - takes value > 0
        '''
        # clearing out the summary browser
        self.sam_summary_out_txt_brow.clear()

        # Takes the user input and send it to sa_module_response_execute
        self.funcs.sa_module_response_execute(True,
                                              False,
                                              self.sam_prcntl_func_trnx_amt_ledit.text(),
                                              self.sam_std_dev_ledit.text(),
                                              self.sam_avg_mnth_trnx_cbox.isChecked())
        return

    def export_button_sa_module(self):
        '''This method takes the output from the backend statistical analysis module and send it to write_excel
        in Funcs class'''
        excel_output = self.funcs.sa_module_generate_output()
        self.funcs.write_excel(excel_output)
        return

    def summary_button_sa_module(self):
        ''' This method displays the summary of statistical module'''
        self.sam_summary_out_txt_brow.clear()
        # sa_summary html is the summary output
        sa_summary_html = self.funcs.sa_module_summary_button_execute(self.sam_percentile_rbtn.isChecked(),
                                                                      self.sam_std_dev_rbtn.isChecked(),
                                                                      self.sam_avg_mnth_trnx_rbtn.isChecked())
        # Converting the summary into html and displaying it on text browser
        self.sam_summary_out_txt_brow.setHtml(sa_summary_html)
        return

    ### Scenario Module

    def sm_sc_module_init(self):
        ''' There are five sub scenario in scenario module
        This method initialises all the five scenarios '''

        #Initialising large transaction analysis module
        self.sm_sc0_module_init()
        # Initialising the large transaction module
        self.sm_sc1_module_init()
        # Initialising the large transaction - standard deviation module
        self.sm_sc2_module_init()
        # Initialising the pass through (Cumulative) module
        self.scenario3_module()
        # Initialising the pass through (Individual) module
        self.scenario4_module()


    def sm_sc0_module_init(self):
        '''This method is initialised for scenario 0- large transaction analysis'''

        # setting the validator for minimum transaction threshold
        self.sm_sc0_min_trnx_amt_thld_ledit.setValidator(QDoubleValidator())
        # upload button to upload file of account numbers
        self.sm_sc0_upload_act_nums_btn.clicked.connect(lambda: self.funcs.upload_btn('sm_sc0_upload_act_nums_btn'))
        # run button on click event triggers the run_button_sc0_run_module
        self.sm_sc0_run_btn.clicked.connect(self.run_button_sc0_run_module)
        # run button on click event triggers the error handling function
        self.sm_sc0_run_btn.clicked.connect(self.funcs.sm_sc0_error_handling)
        # export button on click event triggers the export function in classes
        self.sm_sc0_dexport_btn.clicked.connect(lambda: self.funcs.sm_sc_export_op('s0'))

    def run_button_sc0_run_module(self):
        '''This method updates the dictionary with the recent user inputs'''
        # sm_sc0_input_dict contains the user input as values and widget name as key
        # key = sm_sc0_popltn_rbtn (choosing analysis at population level) and value is boolean
        self.funcs.sm_sc0_input_dict['sm_sc0_popltn_rbtn'] = self.sm_sc0_popltn_rbtn.isChecked()
        # key = sm_sc0_account_rbtn (choosing analysis at account level) and value is boolean
        self.funcs.sm_sc0_input_dict['sm_sc0_account_rbtn'] = self.sm_sc0_account_rbtn.isChecked()
        # key = sm_sc0_min_trnx_amt_thld_ledit and value is user input
        self.funcs.sm_sc0_input_dict['sm_sc0_min_trnx_amt_thld_ledit'] = self.sm_sc0_min_trnx_amt_thld_ledit.text()


    def sm_sc1_module_init(self):
        ''' This method initialises the scenario1- Large transaction'''
        # setting validator for minimum transaction threshold
        self.sm_sc1_min_trnx_amt_thld_ledit.setValidator(QDoubleValidator())
        # setting validator for in threshold cumulative transaction threshold
        self.sm_sc1_incum_trnx_amt_thld_ledit.setValidator(QDoubleValidator())
        # setting validator for out threshold cumulative transaction threshold
        self.sm_sc1_outcum_trnx_amt_thld_ledit.setValidator(QDoubleValidator())
        # setting validator for in and out minimum transaction threshold
        self.sm_sc1_inoutcum_trnx_amt_thld_ledit.setValidator(QDoubleValidator())
        # setting validator for look-back period transaction threshold
        self.sm_sc1_lk_bck_prd_ledit.setValidator(QIntValidator())
        # upload button to upload file of account numbers
        self.sm_sc1_upload_act_nums_btn.clicked.connect(lambda: self.funcs.upload_btn('sm_sc1_upload_act_nums_btn'))
        # run button on click triggers the run_button_sc1_run_module
        self.sm_sc1_run_btn.clicked.connect(self.run_button_sc1_run_module)
        # run button on click triggers the sm_sc1_error_handling
        self.sm_sc1_run_btn.clicked.connect(self.funcs.sm_sc1_error_handling)
        # run button on click triggers the export function
        # Argument:'s1' for scenario1
        self.sm_sc1_dexport_btn.clicked.connect(lambda: self.funcs.sm_sc_export_op('s1'))


    def run_button_sc1_run_module(self):
        '''This method updates the dictionary with the recent user inputs'''
        # sm_sc1_input_dict contains the user input as values and widget name as key
        # key = sm_sc1_popltn_rbtn(choosing analysis at population level) and value is boolean
        self.funcs.sm_sc1_input_dict['sm_sc1_popltn_rbtn'] = self.sm_sc1_popltn_rbtn.isChecked()
        # key = sm_sc1_account_rbtn (choosing analysis at account level) and value is boolean
        self.funcs.sm_sc1_input_dict['sm_sc1_account_rbtn'] = self.sm_sc1_account_rbtn.isChecked()
        # key = sm_sc1_min_trnx_amt_thld_ledit (minimum transaction threshold) and value is user input
        self.funcs.sm_sc1_input_dict['sm_sc1_min_trnx_amt_thld_ledit'] = self.sm_sc1_min_trnx_amt_thld_ledit.text()
        # key = sm_sc1_ref_dt_dateEdit(reference date) and value is user input
        self.funcs.sm_sc1_input_dict['sm_sc1_ref_dt_dateEdit'] = self.sm_sc1_ref_dt_dateEdit.text()
        # key = sm_sc1_lk_bck_prd_ledit(lookback period) and value is user input
        self.funcs.sm_sc1_input_dict['sm_sc1_lk_bck_prd_ledit'] = self.sm_sc1_lk_bck_prd_ledit.text()
        # key = sm_sc1_ref_date_cbox(checkbox for reference date) and value is boolean
        self.funcs.sm_sc1_input_dict['sm_sc1_ref_date_cbox'] = self.sm_sc1_ref_date_cbox.isChecked()
        # key = sm_sc1_incum_trnx_amt_thld_ledit(in threshold cumulative transaction threshold) and value is user input
        self.funcs.sm_sc1_input_dict['sm_sc1_incum_trnx_amt_thld_ledit']= self.sm_sc1_incum_trnx_amt_thld_ledit.text()
        # key = sm_sc1_incum_trnx_amt_thld_ledit(out threshold cumulative transaction threshold) and value is user input
        self.funcs.sm_sc1_input_dict['sm_sc1_outcum_trnx_amt_thld_ledit'] = self.sm_sc1_outcum_trnx_amt_thld_ledit.text()
        # key = sm_sc1_incum_trnx_amt_thld_ledit(in and out minimum transaction threshold) and value is user input
        self.funcs.sm_sc1_input_dict['sm_sc1_inoutcum_trnx_amt_thld_ledit'] = self.sm_sc1_inoutcum_trnx_amt_thld_ledit.text()

    def sm_sc2_module_init(self):
        ''' This method initialises the scenario2- Large transaction(standard deviation) '''

        # setting validator for in standard deviation threshold
        self.sm_sc2_instd_dev_ledit.setValidator(QDoubleValidator())
        # setting validator for out standard deviation threshold
        self.sm_sc2_outstd_dev_ledit.setValidator(QDoubleValidator())
        # setting validator for minimum transaction threshold
        self.sm_sc2_min_trnx_amt_thld_ledit.setValidator(QDoubleValidator())
        # setting validator for look back period
        self.sm_sc2_lk_bck_prd_ledit.setValidator(QIntValidator())
        # setting validator for in ann out standard deviation
        self.sm_sc2_inoutstd_dev_ledit.setValidator(QDoubleValidator())
        # setting validator for in threshold
        self.sm_sc2_thld_in_ledit.setValidator(QDoubleValidator())
        # setting validator for out threshold
        self.sm_sc2_thld_out_ledit.setValidator(QDoubleValidator())
        # setting validator for in and out threshold
        self.sm_sc2_thld_in_out_ledit.setValidator(QDoubleValidator())
        # upload button to upload file of account numbers
        self.sm_sc2_upload_act_nums_btn.clicked.connect(lambda: self.funcs.upload_btn('sm_sc2_upload_act_nums_btn'))
        # run button on click triggers the run_button_sc2_run_module
        self.sm_sc2_run_btn.clicked.connect(self.run_button_sc2_run_module)
        # run button on click triggers the sm_sc2_error_handling
        self.sm_sc2_run_btn.clicked.connect(self.funcs.sm_sc2_error_handling)
        # export button on click triggers the export result in funcs class
        # Argument:'s2' for scenario2
        self.sm_sc2_dexport_btn.clicked.connect(lambda: self.funcs.sm_sc_export_op('s2'))

    def run_button_sc2_run_module(self):
        '''This method takes the recent user input from the front end and updates the dictionary'''
        # key = sm_sc2_popltn_rbtn(choosing analysis at population level) and value is boolean
        self.funcs.sm_sc2_input_dict['sm_sc2_popltn_rbtn'] = self.sm_sc2_popltn_rbtn.isChecked()
        # key = sm_sc2_account_rbtn (choosing analysis at account level) and value is boolean
        self.funcs.sm_sc2_input_dict['sm_sc2_account_rbtn'] = self.sm_sc2_account_rbtn.isChecked()
        # key = sm_sc2_min_trnx_amt_thld_cbox (minimum transaction threshold checkbox) and value is boolean
        self.funcs.sm_sc2_input_dict['sm_sc2_min_trnx_amt_thld_cbox'] = self.sm_sc2_min_trnx_amt_thld_cbox.isChecked()
        # key = sm_sc2_min_trnx_amt_thld_ledit (minimum transaction threshold ) and value is user input
        self.funcs.sm_sc2_input_dict['sm_sc2_min_trnx_amt_thld_ledit'] = self.sm_sc2_min_trnx_amt_thld_ledit.text()
        # key = sm_sc2_ref_date_cbox (reference date checkbox ) and value is boolean
        self.funcs.sm_sc2_input_dict['sm_sc2_ref_date_cbox'] = self.sm_sc2_ref_date_cbox.isChecked()
        # key = sm_sc2_ref_dt_dateEdit (reference data) and value is user input
        self.funcs.sm_sc2_input_dict['sm_sc2_ref_dt_dateEdit'] = self.sm_sc2_ref_dt_dateEdit.text()
        # key = sm_sc2_lk_bck_prd_ledit (look back period) and value is user input
        self.funcs.sm_sc2_input_dict['sm_sc2_lk_bck_prd_ledit'] = self.sm_sc2_lk_bck_prd_ledit.text()
        # key = sm_sc2_instd_dev_ledit (in standard deviation) and value is user input
        self.funcs.sm_sc2_input_dict['sm_sc2_instd_dev_ledit'] = self.sm_sc2_instd_dev_ledit.text()
        # key = sm_sc2_outstd_dev_ledit (out standard deviation) and value is user input
        self.funcs.sm_sc2_input_dict['sm_sc2_outstd_dev_ledit'] = self.sm_sc2_outstd_dev_ledit.text()
        # key = sm_sc2_inoutstd_dev_ledit (in and out standard deviation) and value is user input
        self.funcs.sm_sc2_input_dict['sm_sc2_inoutstd_dev_ledit'] = self.sm_sc2_inoutstd_dev_ledit.text()
        # key = sm_sc2_thld_in_ledit (in threshold) and value is user input
        self.funcs.sm_sc2_input_dict['sm_sc2_thld_in_ledit'] = self.sm_sc2_thld_in_ledit.text()
        # key = sm_sc2_thld_out_ledit (out standard deviation) and value is user input
        self.funcs.sm_sc2_input_dict['sm_sc2_thld_out_ledit'] = self.sm_sc2_thld_out_ledit.text()
        # key = sm_sc2_thld_in_out_ledit (in and out standard deviation) and value is user input
        self.funcs.sm_sc2_input_dict['sm_sc2_thld_in_out_ledit'] = self.sm_sc2_thld_in_out_ledit.text()


    def scenario3_module(self):
        # setting validator for cumulative transaction threshold
        self.sm_sc3_cum_trnx_amt_thld_ledit.setValidator(QDoubleValidator())
        # setting validator for look back period
        self.sm_sc3_lk_bck_prd_ledit.setValidator(QIntValidator())
        # setting validator for minimum transaction threshold
        self.sm_sc3_min_trnx_amt_thld_ledit.setValidator(QDoubleValidator())
        # run button on click triggers the run_button_scenario3_module
        self.sm_sc3_run_btn.clicked.connect(self.run_button_scenario3_module)
        # click on data export triggers the sm_sc_export_op function in Funcs class
        # Argument:'s3' for scenario3
        self.sm_sc3_dexport_btn.clicked.connect(lambda: self.funcs.sm_sc_export_op('s3'))

    def run_button_scenario3_module(self):
        '''This method takes the updated user input from the front end and send it to error_handling_scenario3'''

        #Arguments:
        # key = sm_sc3_min_trnx_amt_thld_cbox (minimum transaction threshold checkbox) and value is boolean
        # key = sm_sc3_min_trnx_amt_thld_ledit (minimum transaction threshold) and value is user input
        # key = sm_sc3_ref_date_cbox (reference date checkbox) and value is boolean
        # key = sm_sc3_ref_dt_dateEdit (reference date) and value is user input
        # key = sm_sc3_lk_bck_prd_ledit (lookback period) and value is user input
        # key = sm_sc3_cum_trnx_amt_thld_ledit (cumulative transaction threshold) and value is user input
        # key = sm_sc3_min_range_sbox (minimum range spinbox) and value is user input (can be >0 and <=1000)
        # key = sm_sc3_max_range_sbox (maximum range spinbox) and value is user input (can be >0 and <=1000)
        self.funcs.error_handling_scenario3({
                                                 'sm_sc3_min_trnx_amt_thld_cbox': self.sm_sc3_min_trnx_amt_thld_cbox.isChecked(),
                                                 'sm_sc3_min_trnx_amt_thld_ledit': self.sm_sc3_min_trnx_amt_thld_ledit.text(),
                                                 'sm_sc3_ref_date_cbox': self.sm_sc3_ref_date_cbox.isChecked(),
                                                 'sm_sc3_ref_dt_dateEdit': self.sm_sc3_ref_dt_dateEdit.text(),
                                                 'sm_sc3_lk_bck_prd_ledit': self.sm_sc3_lk_bck_prd_ledit.text(),
                                                 'sm_sc3_cum_trnx_amt_thld_ledit': self.sm_sc3_cum_trnx_amt_thld_ledit.text(),
                                                 'sm_sc3_min_range_sbox': self.sm_sc3_min_range_sbox.value(),
                                                 'sm_sc3_max_range_sbox': self.sm_sc3_max_range_sbox.value()})
        return

    def scenario4_module(self):
        # setting validator for cumulative transaction threshold
        self.sm_sc4_cum_trnx_amt_thld_ledit.setValidator(QDoubleValidator())
        # setting validator for look back period
        self.sm_sc4_lk_bck_prd_ledit.setValidator(QIntValidator())
        # setting validator for minimum transaction amount threshold
        self.sm_sc4_min_trnx_amt_thld_ledit.setValidator(QDoubleValidator())
        # run button on click triggers the run_button_scenario4_module
        self.sm_sc4_run_btn.clicked.connect(self.run_button_scenario4_module)
        # click on data export triggers the sm_sc_export_op function in Funcs class
        # Argument:'s4' for scenario4
        self.sm_sc4_dexport_btn.clicked.connect(lambda: self.funcs.sm_sc_export_op('s4'))

    def run_button_scenario4_module(self):
        '''This method takes the updated user input from the front end and send it to error_handling_scenario4'''

        # Arguments:
        # key = sm_sc4_flagged_trans_cbox (previously flagged transactions) and value is boolean
        # key = sm_sc4_min_trnx_amt_thld_ledit (minimum transaction threshold) and value is user input
        # key = sm_sc4_ref_date_cbox (reference date checkbox) and value is boolean
        # key = sm_sc4_ref_dt_dateEdit (reference date) and value is user input
        # key = sm_sc4_lk_bck_prd_ledit (lookback period) and value is user input
        # key = sm_sc4_cum_trnx_amt_thld_ledit (cumulative transaction threshold) and value is user input
        # key = sm_sc4_min_range_sbox (minimum range spinbox) and value is user input (can be >0 and <=1000)
        # key = sm_sc4_max_range_sbox (maximum range spinbox) and value is user input (can be >0 and <=1000)
        self.funcs.error_handling_scenario4({
                                            'sm_sc4_flagged_trans_cbox': self.sm_sc4_flagged_trans_cbox.isChecked(),
                                             'sm_sc4_min_trnx_amt_thld_ledit': self.sm_sc4_min_trnx_amt_thld_ledit.text(),
                                             'sm_sc4_ref_date_cbox': self.sm_sc4_ref_date_cbox.isChecked(),
                                             'sm_sc4_ref_dt_dateEdit': self.sm_sc4_ref_dt_dateEdit.text(),
                                             'sm_sc4_lk_bck_prd_ledit': self.sm_sc4_lk_bck_prd_ledit.text(),
                                             'sm_sc4_cum_trnx_amt_thld_ledit': self.sm_sc4_cum_trnx_amt_thld_ledit.text(),
                                             'sm_sc4_min_range_sbox': self.sm_sc4_min_range_sbox.value(),
                                             'sm_sc4_max_range_sbox': self.sm_sc4_max_range_sbox.value()})
        return

    # visualisation module

    def viz_module(self):

        '''Add validators Here
        connect buttons here
        '''
        self.vis_min_trnx_amt_thld_ledit.setValidator(QDoubleValidator())
        self.vis_imgexport_btn.clicked.connect(self.run_button_viz_module)
        self.vis_upload_act_nums_btn.clicked.connect(self.upload_account_button_viz_module)
        self.vis_trueimgexport_btn.clicked.connect(self.export_image_viz_module)
        self.vis_dataexport_btn.clicked.connect(self.export_data_viz_module)

        return

    def run_button_viz_module(self):
        '''

        Clear Text Window #self.sam_summary_out_txt_brow.clear()
        Run execute  Supply Widget Inputs ###self.funcs.sa_module_response_execute(True,
                                              False,
                                              self.sam_prcntl_func_trnx_amt_ledit.text(),
                                              self.sam_std_dev_ledit.text(),
                                              self.sam_avg_mnth_trnx_cbox.isChecked())

        Show New Rendered HTML Import Directly from Module #

        '''
        print('Ui Run Visualisation')
        self.vis_smpl_export_txt_brow.clear()
        self.funcs.viz_module_response_execute(self.vis_min_trnx_amt_thld_cbox.isChecked(),
                                               self.vis_min_trnx_amt_thld_ledit.text(),
                                               self.vis_star_dt_dateEdit.text(),
                                               self.vis_end_dt_dateEdit.text())

        self.vis_smpl_export_txt_brow.setHtml(self.funcs.model.viz_m.img_html)

        return

    def upload_account_button_viz_module(self):
        '''uploading the account numbers file'''
        account_path = self.funcs.upload_btn_viz()
        if account_path is not None:
            self.funcs.model.update_acc_visualisation(account_path)

        return

    def export_data_viz_module(self):
        '''
        Export flat data from viz_module
        '''
        export_dict = {'Flat Output':self.funcs.model.viz_m.output_flat,
        'Aggregated Output':self.funcs.model.viz_m.output_aggregated}
        ### Consider Moving this line to write excel Functio
        if all(value is None for value in export_dict.values()):
            export_dict = None
        self.funcs.write_excel(export_dict)
        return
    def export_image_viz_module(self):
        '''
        Export image in png/jpg format
        '''
        self.funcs.write_image(self.funcs.model.viz_m.output_img)

# Sanctioned countries
    def sanctiond_ctry_init(self):
        # click on run button triggers the sanctioned_ctry_run'''
        self.sc_run_btn.clicked.connect(self.funcs.sanctioned_ctry_run)
        # click on data export button triggers the SHRC_export_file  '''
        self.sc_dexport_btn.clicked.connect(self.funcs.SHRC_export_file)

    def del_pickle_file(self):
        '''This function deletes the tms_app directory'''
        path_to_desktop_tms_app = os.path.join(os.getcwd(), "tms_app")
        shutil.rmtree(path_to_desktop_tms_app, ignore_errors=True, onerror=None)
