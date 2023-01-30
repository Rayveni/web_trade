from flask import flash

def flash_complex_result(error,result,success_msg:str='success'):   
        if not error[0]:
		
            flash(error[1],'error')  #success info error  
        elif not result[0]:
    	
            flash(result[1],'error')  #success info error
        else:
   		
            flash(success_msg,'success')  #success info error 
