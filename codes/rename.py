'''
Renaming the columns of dataframe 
'''

rename_column_mapping ={
    'B1':{
                'Group No.':'groupnumber',
                'Section No.':'sectionnumber', 
                'Section Description':'sectiondescription', 
                'BA No.':'bano', 
                'BA Description':'badescription', 
                'rollupbano':'rollupbano', 
                'rollupbadescription':'rollupbadescription',
                'BA Product':'baproduct', 
                'Billing Category No':'billingcategory', 
                'Billing Category Description':'categorydescription',
                'rollupbillingcategory':'rollupbillingcategory', 
                'rollupcategorydescription':'rollupcategorydescription',
                'statusid':'statusid', 
                'Billing Profile':'statusname', 
                'remarks':'remarks', 
                'drop_yn':'drop_yn'
    },
    'B2':{
                'Group No.':'groupnumber',
                'Section No.':'sectionnumber', 
                'Section Description':'sectiondescription', 
                'BA No.':'bano', 
                'BA Description':'badescription', 
                'BA Product':'baproduct', 
                'Billing Category No':'billingcategory', 
                'Billing Category Description':'categorydescription',
                'statusid':'statusid',
                'statusname': 'statusname',
                'groupname':'groupname',
                'remarks':'remarks', 
                'drop_yn':'drop_yn'
    }    
}


