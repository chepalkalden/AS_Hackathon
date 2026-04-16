insert_dict = {
    'TX': """
        INSERT INTO HR_TX (
            groupnumber,
            sectionnumber,
            sectiondescription,
            bano,
            badescription,
            rollupbano,
            rollupbadescription,
            baproduct,
            billingcategory,
            categorydescription,
            rollupbillingcategory,
            rollupcategorydescription,
            statusid,
            statusname,
            remarks,
            drop_yn
        )
        VALUES (
            :groupnumber,
            :sectionnumber,
            :sectiondescription,
            :bano,
            :badescription,
            :bano,
            :badescription,
            :baproduct,
            :billingcategory,
            :categorydescription,
            :billingcategory,
            :categorydescription,
            substr(:statusname, 1, 3),
            :statusname,
            :remarks,
            'N'
        )
    """,
    'IL': """
        INSERT INTO HR_IL (
            groupnumber,
            sectionnumber,
            sectiondescription,
            bano,
            badescription,
            baproduct,
            billingcategory,
            categorydescription,
            statusid,
            statusname,
            groupname,
            remarks,
            drop_yn
        )
        VALUES (
            :groupnumber,
            :sectionnumber,
            :sectiondescription,
            :bano,
            :badescription,
            :baproduct,
            :billingcategory,
            :categorydescription,
            substr(:statusname, 1, 3),
            :statusname,
            NULL,
            :remarks,
            'N'
        )
    """       
}

