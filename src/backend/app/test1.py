

def deserializer(value, key):
    values_list = value.split(',')
    result = zip(key, values_list)
    return dict(result)
    
if __name__ == "__main__":
    value = "09363261462,alirez m3ortezaei,parvaz@exa2mple.com,parvaz_2324"
    key = ['phone_number', 'full_name', 'email', 'password']
    p = deserializer(value, key)
    print(p)