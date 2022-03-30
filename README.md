## **Visão Geral**

O **authentication-app-cs-plugin** adiciona em uma stack a capacidade de verificar se um usuário possui acesso a um determinado recurso restrito trazendo segurança para sua API.

Para aplicar o plugin execute o comando:
```
$ stk apply plugin skynet-dotnet-stack/authentication-app-cs-plugin
```
### **Pré-requisitos**
Para utilizar esse plugin é necessário ter uma stack dotnet criada pelo CLI do StackSpot que você pode baixar [**aqui**](https://stackspot.com.br/).

Ter instalado:
- .NET 5 ou 6 
- O template base de `rest-app-cs-template` já deverá estar aplicado para você conseguir utilizar este plugin. 

### **Inputs**
Os inputs necessários para utilizar o plugin são:
| **Campo** | **Valor** | **Descrição** |
| :--- | :--- | :--- |
| Url | https://myauthenticationserver/token | Url de seu servidor de autenticação/autorização |

#### Uso

Adicione ao seu `IServiceCollection` via `services.AddTokenAuthentication()` no `Startup` da aplicação ou `Program` tendo como parametro de entrada a `url` do seu provedor de Autenticação e Autorização. 

```csharp
services.AddTokenAuthentication(url);
```
> Caso encontre o erro *`System.ArgumentOutOfRangeException: Valid values are between -62135596800 and 253402300799, inclusive. (Parameter 'seconds')`* utilize a sobrecarga do serviço definindo o parametro `ConvertExpirationMillisecondsToSeconds` como `true`.  
Isso ocorre somente em casos muito específicos.

```csharp
services.AddTokenAuthentication(serverAuthenticatonUrl,
                                new HttpClientHandlerOptions()
                                {
                                    ConvertExpirationMillisecondsToSeconds = true
                                });
```

### Configurações Adicionais

*  Definir o `[Authorize]` para suas `Controllers` e/ou `Endpoints`. 

```csharp
[Authorize]
public class MyController : ControllerBase
{
    ...
}
```

*  Em seu arquivo `Startup` ou `Program` garantir as configurações básicas de ApplicationBuilder para `app.Authorization()` e `app.Authentication()`. 

```csharp
...
app.UseRouting();

app.UseAuthentication();
app.UseAuthorization();

app.UseEndpoints();
...
```

*  E também configurar sua `IServiceCollection` para que as Controllers possuam o filtro de Autorização.

```csharp
...
services.AddControllers(options => 
{
    options.Filters.Add(new AuthorizeFilter());

});
...
```

*  Se utilizar o Swagger em sua aplicação, configure as definições de segurança para a autenticação. Exemplo: 

```csharp
...
services.AddSwaggerGen(c => 
{
    c.SwaggerDoc("v1", new OpenApiInfo { Title = "MyApi", Version = "v1" })
    c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme()
    {
        In = ParameterLocation.Header,
        Description = "Autenticação com Token",
        Name = "Authorization",
        Type = SecuritySchemeType.OAuth2
    });
});
...
```
