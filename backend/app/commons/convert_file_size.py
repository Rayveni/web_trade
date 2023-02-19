def convert_file_size(size_bytes:float,round_ndigits:int=2)->str:
    size_name = ("B", "KB", "MB", "GB")
    _step=1024
    prev_res=size_bytes
    for i in range(len(size_name)):
        size_bytes=size_bytes/_step
        if size_bytes<1:
            break
        prev_res=size_bytes
    return f'{round(prev_res,round_ndigits)}{size_name[i]}'