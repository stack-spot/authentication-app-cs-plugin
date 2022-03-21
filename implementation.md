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

### Configurações Adicionais

*  Definir o `[Authorize]` para suas `Controllers` e/ou `Endpoints`. 

```csharp
[Auhtorize]
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