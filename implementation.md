### **Inputs**
Os inputs necessários para utilizar o plugin são:  

| **Campo** | **Valor** | **Descrição** |
| :--- | :--- | :--- |
| Url | https://myauthenticationserver/token | Url do servidor de autenticação/autorização |

#### Uso

Adicione ao seu `IServiceCollection`, via `services.AddTokenAuthentication()`. no `Startup` da aplicação ou `Program`. Tenha como parâmetro de entrada a `url` do seu provedor de Autenticação e Autorização. 

```csharp
services.AddTokenAuthentication(url);
```

> Caso encontre o erro *`System.ArgumentOutOfRangeException: Valid values are between -62135596800 and 253402300799, inclusive. (Parameter 'seconds')`* Utilize a sobrecarga do serviço definindo o parâmetro `ConvertExpirationMillisecondsToSeconds` como `true`.  
Isto ocorre somente em casos muito específicos. Confira o exemplo abaixo:  

```csharp
services.AddTokenAuthentication(serverAuthenticatonUrl,
                                new HttpClientHandlerOptions()
                                {
                                    ConvertExpirationMillisecondsToSeconds = true
                                });
```

### Configurações Adicionais

Siga os seguintes passos para fazer configurações adicionais no plugin:  

1. Defina o `[Authorize]` para suas `Controllers` e/ou `Endpoints`. 

```csharp
[Authorize]
public class MyController : ControllerBase
{
    ...
}
```

2. Em seu arquivo `Startup` ou `Program`, garanta as configurações básicas de **ApplicationBuilder** para `app.Authorization()` e `app.Authentication()`. 

```csharp
...
app.UseRouting();

app.UseAuthentication();
app.UseAuthorization();

app.UseEndpoints();
...
```

3. Configure a `IServiceCollection` para que as Controllers tenham o filtro de Autorização.

```csharp
...
services.AddControllers(options => 
{
    options.Filters.Add(new AuthorizeFilter());

});
...
```