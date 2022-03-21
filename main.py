from templateframework.runner import run
from templateframework.template import Template
from templateframework.metadata import Metadata
import subprocess
import json
import os

def put_appsettings(project_name: str, target_path: str, url: str, file_name: str):
        os.chdir(f'{target_path}/src/{project_name}.Api/')
        print(f'Setting {file_name}...')

        with open(file=file_name, encoding='utf-8-sig', mode='r+') as appsettings_json_file:
            appsettings_json_content = json.load(appsettings_json_file)
            appsettings_json_content.update({
                                                "Authentication" : {
                                                    "Url": f"{url}"
                                                }
                                            })                                         
            appsettings_json_file.seek(0)
            json.dump(appsettings_json_content, appsettings_json_file, indent=2)
        print(f'Setting {file_name} done.')   

class Plugin(Template):
    def post_hook(self, metadata: Metadata):
        project_name = metadata.global_inputs['project_name']
        url = metadata.inputs['url']
        using = f"using StackSpot.Authentication;\n"
        param_configuration = f"string url = configuration.GetSection(\"Authentication:Url\").Value"
        service_cache = f"services.AddDistributedMemoryCache()"
        service_auth = f"services.AddTokenAuthentication(url)"
        
        put_appsettings(project_name, metadata.target_path, url, 'appsettings.json')
        put_appsettings(project_name, metadata.target_path, url, 'appsettings.Development.json')   
        
        print('Adding Package...')
        subprocess.run(['dotnet', 'add', 'package', 'StackSpot.Authentication'])

        print('Setting Configuration...')

        os.chdir(f'{metadata.target_path}/src/{project_name}.Api/')
        configuration_file = open(file='ConfigurationStackSpot.cs', mode='r')
        content = configuration_file.readlines()
        index = [x for x in range(len(content)) if 'return services' in content[x].lower()]
        content[0] = using+content[0]
        content[index[0]] = f"{param_configuration};\n{service_cache};\n{service_auth};\n{content[index[0]]}"
        
        configuration_file = open(file='ConfigurationStackSpot.cs', mode='w')                     
        configuration_file.writelines(content)
        configuration_file.close()

        print('Setting Configuration done.') 

        print('Apply dotnet format...')
        os.chdir(f'{metadata.target_path}/')
        subprocess.run(['dotnet', 'dotnet-format', './src'])   
        print('Apply dotnet format done...')

if __name__ == '__main__':
    run(Plugin())
