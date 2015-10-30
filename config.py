'''Variables:
clientid:         API key
clientsecret:     API secret
host:             API host
search_field      Server attribute to apply search_string to (server_label|hostname|reported_fqdn|group_name)
output            Output format: (html|pdf|text)
logo_url          URL or path for logo image.  If you are using a proxy and output='pdf', you must load the logo file from the local filesystem.
prox_host         Proxy host IP or host name.  No protocol- HTTPS is assumed. 
prox_port         Valid value here is 1-65535 or ''
'''
clientid     = 'ABCD1234'
clientsecret = '12345678123456781234567812345678'
