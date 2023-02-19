from app.attributes import upload_table_info

def update_upload_table_info(db_manager,sys_name:str,actual_date):
    row=upload_table_info(sys_name,actual_date)
    r=db_manager.insert_into_table_from_attr(table_name='upload_info',data_attr=row,update_criteria={"sys_name":sys_name} )
    return r
