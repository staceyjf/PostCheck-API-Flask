# Welcome to PostChecker-API-Flask

A Flask and MySQL REST API that provides clients with an easy way to source and query postcode and suburb information.

Deployed at: https://www.staceyfanner.com/Postcheck-front/

_Please note that I am using the free tier of Azure Web app so it can take a while to load_

## The Brief

In this fictional brief, Aus-Post wants to add authentication to their service (particularly for the creation, updating, and deletion functionalities) that provides postcode and suburb information via an API.

The MVP to deliver on this client brief was:

- Create an API that allows clients to retrieve and add suburb and postcode combinations.
- Implement:
  - An API that allows clients to retrieve suburb information by postcode.
  - An API that allows clients to retrieve a postcode given a suburb name.
- A secured API to add new suburb and postcode combinations.
- Some form of persistence (a database).

Additional areas to explore:

- Implement:
  - A basic reporting endpoint powered via a PySpark data pipeline. The python script can be viewed here: (available [here](https://github.com/staceyjf/SuburbSavvy))

## Demo

This API works hand in hand with this Typescript React app (available [here](https://github.com/staceyjf/Postcheck-front)) which is being demo'ed below.

<div align="center">
  <img src="./planning /postcheckAPI.gif" alt="Homepage">
</div>

## Build Steps

```bash
1. Clone the repo.
2. Cd into `PostCheck-API-Flask` folder
3. Set up the virtual envs with with `pipenv install` and activate the virtual environment with `pipenv shell` \*
4. Add your credential in a .env to connect to a mySQL database. An example env configure can be found at `env_example.txt`
5. Start the production web server with via `gunicorn manage:app` \*
```

_Note: The above steps assume that you already have `pipenv` installed. If you prefer, you can replace pipenv with your tool of choice for managing virtual environments.e_
_Note: While I have selected a lower worker setting, review this in relation to your hardware and adjust accordingly_

## Planning considerations

### ERD

Understanding the relationship of the data was an important starting place and took the following steps as a result:

1. PostcodeSuburbMapping was the join table, which SQLAlchemy then managed.
2. Bi-directional relationship between Postcodes and Suburbs, for improved ease of querying as each entity is directly accessible through the other.

<div align="center">
  <img src="./planning /postcheck_erd.png" style="max-width: 800px;" alt="ERD for postcheck API">
</div>

### Design choices

1. **RESTful API Design:** Felt like a natural fit given its wide spread adoption, compatibility and simplicity (leveraging std HTTP methods to interact with resources).

2. **Adopting the Controller-Service-Repository Pattern:** This layered architecture approach ensured clear separation of concerns, leading to better-organized and more maintainable code.

3. **Modular Services Architecture:** The use of factory functions in create_app() and utilizing Flask-Smorest's blueprints enabled the API to be divided into loosely coupled components, with each service focused on a specific entity (Postcodes, Suburbs, Users, and Reporting).

4. **Authentication:** Following a discussion with my _nology coach, we agreed it would be beneficial for my overall learning to implement token-based JWT authentication, even though a service authentication approach like API keys linked to subscriptions might be more relevant for this type of API service.

5. **Cloud Services:** As I am studying to complete the Azure Cloud Fundamentals certification, I wanted to apply my theoretical knowledge in practice so I utilized Azure Web App for deployment.

which manifested into a flow of data via the following layers:

<div align="center" style="background: white">

[![](https://mermaid.ink/img/pako:eNqVVm1v6jYU_itHubrSJrVCWr9sVJoESSm00KYErR9ChdzEAQsnzmynXHZz__tO4gQMTbvdSAjH5_F5y-PH_u5EIqZO31lLkm9g4V0vM8Dn61fwaMIyCnqDP5EDJ3sq4RdfUkUzTTQTWc_lDMcwrUy_moWqeDWubODKAFc10OCqZxDOKYl0b7HPaRBJluveA3sTLwZBs3iZdWWTsjjmtE3InfRcD3yWU14BSBbDkERbXN2dlztZud6qxR-TmYW3TI-LVxhEVcrq5Wh6CINM7BJOthR-hynLNMvWlv0x9ARGlDAsGI8tgx_6hdpg-2DwTyEpuAIbglElzOmaKS33Fvgp9GjOxf4If6aYTZ6_78ehmPlNsEgKvhr4k1VT9XmTb0J_f_e8sAJNwmBH1msqrbkAUXojsroEfckymIoGcgQde4h1SME5lefRqmcYjjhRW8CkYMf0BurXyyAVSAkNPZgRqTYp4VzsrBTq-tqXjqABlW8sol0R3XBYKOyrUlXaLPoJr3OaC8W0kPsux14YPE0HPNrQdA-P89nLqfkuHHCavrII3hgxZcKMoeOKQV1JfMjpV6G1SFtOe0STV6Jorxocud3J5wqC3169a8wonO0xe2idWfnch75Qei1ph72LZnUMX4oIO4zU79g9U-RPkBO5_cxLTe-0QwhiJmm962AxPM7ehv9j14wbEO6TliGd-oFOMhNDQSKx1bY-mc5WG-9EOsziAVxe_lmOFwsf4_9dIIVVCcNGJ4eVEUqPcrommir0UYLbGF1jnGSaStQ5Ve-GElqN9Yz5qaCSUfQ5aubvzPyMZGSNHg-EsiBN2DGqHUfIoEAOoSpFNa6Em24YqlSRtjWXMOlGVRsfP3IJwZnddEDlmAktYXD9WXcNcQ-MOXIYe9wSzm7yfd1kPA5i46CEaRN9WlueJWu7e39icDklGLSOV2m_BRydAI1vN_irhHmIfzBinL58WsTZ0VKlfqCwnfzMNGhe4EIkU6v5MyRtCQ9NFg8G1JweJTw2849mvj46oDlHJil--RL8BuIbSO23NtXl3TbW25aC9eFhe6hh4wY2tmE0hgXanuzyH_OqdML7MIhjIBBhZyUIGaO7REiUOFUQjtMEW7w3y_BFKZSx6oZg9lDCOO9_Sf5ILnCjii3tf7m6umrGlzsW603_t_zb9dlyc6TbHqLo5zwYAT3xkET_5cHy8fF95VCbHfLsGmEXcAL78ID-cMWZntuFvcd1aPLHC87k9wzoXDgplSlhMd4Gv1cLlw6qSkqXTh-HMU1IwfXSWWY_EEoKLYJ9Fjl9LQt64UhRrDdOPyFc4VuRxyiGHiOoXOlhlsbVOTsz98362vnjXxr6Xho?type=png)](https://mermaid.live/edit#pako:eNqVVm1v6jYU_itHubrSJrVCWr9sVJoESSm00KYErR9ChdzEAQsnzmynXHZz__tO4gQMTbvdSAjH5_F5y-PH_u5EIqZO31lLkm9g4V0vM8Dn61fwaMIyCnqDP5EDJ3sq4RdfUkUzTTQTWc_lDMcwrUy_moWqeDWubODKAFc10OCqZxDOKYl0b7HPaRBJluveA3sTLwZBs3iZdWWTsjjmtE3InfRcD3yWU14BSBbDkERbXN2dlztZud6qxR-TmYW3TI-LVxhEVcrq5Wh6CINM7BJOthR-hynLNMvWlv0x9ARGlDAsGI8tgx_6hdpg-2DwTyEpuAIbglElzOmaKS33Fvgp9GjOxf4If6aYTZ6_78ehmPlNsEgKvhr4k1VT9XmTb0J_f_e8sAJNwmBH1msqrbkAUXojsroEfckymIoGcgQde4h1SME5lefRqmcYjjhRW8CkYMf0BurXyyAVSAkNPZgRqTYp4VzsrBTq-tqXjqABlW8sol0R3XBYKOyrUlXaLPoJr3OaC8W0kPsux14YPE0HPNrQdA-P89nLqfkuHHCavrII3hgxZcKMoeOKQV1JfMjpV6G1SFtOe0STV6Jorxocud3J5wqC3169a8wonO0xe2idWfnch75Qei1ph72LZnUMX4oIO4zU79g9U-RPkBO5_cxLTe-0QwhiJmm962AxPM7ehv9j14wbEO6TliGd-oFOMhNDQSKx1bY-mc5WG-9EOsziAVxe_lmOFwsf4_9dIIVVCcNGJ4eVEUqPcrommir0UYLbGF1jnGSaStQ5Ve-GElqN9Yz5qaCSUfQ5aubvzPyMZGSNHg-EsiBN2DGqHUfIoEAOoSpFNa6Em24YqlSRtjWXMOlGVRsfP3IJwZnddEDlmAktYXD9WXcNcQ-MOXIYe9wSzm7yfd1kPA5i46CEaRN9WlueJWu7e39icDklGLSOV2m_BRydAI1vN_irhHmIfzBinL58WsTZ0VKlfqCwnfzMNGhe4EIkU6v5MyRtCQ9NFg8G1JweJTw2849mvj46oDlHJil--RL8BuIbSO23NtXl3TbW25aC9eFhe6hh4wY2tmE0hgXanuzyH_OqdML7MIhjIBBhZyUIGaO7REiUOFUQjtMEW7w3y_BFKZSx6oZg9lDCOO9_Sf5ILnCjii3tf7m6umrGlzsW603_t_zb9dlyc6TbHqLo5zwYAT3xkET_5cHy8fF95VCbHfLsGmEXcAL78ID-cMWZntuFvcd1aPLHC87k9wzoXDgplSlhMd4Gv1cLlw6qSkqXTh-HMU1IwfXSWWY_EEoKLYJ9Fjl9LQt64UhRrDdOPyFc4VuRxyiGHiOoXOlhlsbVOTsz98362vnjXxr6Xho)
</div>

## Deployment

1. Gunicorn: Utilized Gunicorn, a WSGI HTTP server, to manage requests and responses in a production environment. Gunicorn is preferred over Flask's built-in development server due to its enhanced capability to handle concurrent requests and manage multiple worker processes or threads. Although the current application has a low volume of requests, it was a valuble learning experience to intergrate Guicorn.
2. MySQL Cloud DB: To ensure data persistence for my deployed application, I used Aiven to host the MySQL database. The PostgreSQL database was hosted locally, which imposes limitations on integrating the data pipeline with the app.

## Key Features:

### Back-end

#### The '70':

1. **CRUD API Endpoints**: Developed comprehensive RESTful CRUD (Create, Read, Update, Delete) endpoints for managing Postcodes and Suburbs. This includes the capability to query postcodes by suburb name

2. **API documentation:** Integrated Swagger for clear, interactive API documentation, making it easier to understand and consume the API.

3. **Logging:** Adopted Python's built-in logging module via Flask for basic console-level logging, providing insights into the application's operational status and aiding in troubleshooting.

4. **Database Management:**

   - Employed Alembic via Flask Migrate to maintain the integrity of the data by keeping track and implementing changes to the db's schema through migration scripts.
   - Used SQLAlchemy as the ORM to define and generate the schema.

5. **Response Validation:** Implemented response validation with Marshmallow to reduce errors arising from unexpected request bodies and enhance developer experience by ensuring consistent and validated responses.

6. **Serialization/Deserialization:** Utilized Flask-Smorest to automate the serialization and deserialization of data, reducing the potential for errors that can occur when manually serializing or deserializing data.

7. **Basic Integration Testing:** All endpoints were tested in Postman to ensure that the server, database, and validation mechanisms were functioning correctly.

#### The '20':

1. **Authentication:** Utilized the HS256 algorithm and a secret key for JWT (JSON Web Tokens) authentication with PyJWT, enhancing security by ensuring that certain routes were accessible only to authenticated users.

#### The '10':

1. **Basic Data Processing Pipeline:** Developed a basic data pipeline with PySpark to load a sample dataset into a PostgreSQL database, perform essential data cleaning and preparation tasks, and subsequently write the processed data to PostCheck's MySQL database.

## Key Learning Highlights

1. **External libraries:** While Flask-Smorest did a lot of the heavy lifting with serialising / deserialisng and providing documentation via swagger, it required a class-based approach for my controllers, utilizing Flask's MethodView. Although my preference was for a functional approach to maintain consistency, the benefits offered by Flask-Smorest outweighed my preference for consistency.

2. **Reporting Data:** The process of manipulating data to fit the requirements of Nivo charting tested both my understanding of my validation schemas and my foundational Python skills, particularly in writing loops to restructure data and insert new key-value pairs into each data point dictionary.

3. **CORS:** Despite adding Flask-CORS to handle Cross-Origin Resource Sharing, additional configuration was necessary to bypass the default security restrictions for cross-origin requests.

4. **Avoiding Mixed Media Error:** To ensure that the secure HTTPS requests from my frontend were correctly handled and the application’s responses remained secure, I had to add `ProxyFix` middleware to my Flask app. This middleware helps to properly interpret the headers forwarded by Azure Web App's reverse proxy, ensuring that the X-Forwarded-For, X-Forwarded-Proto, and other headers are correctly processed. This setup helps prevent mixed content warnings by ensuring that the application correctly recognizes and handles secure requests.

## To-Dos

1. **Testing:** Implement unit testing with pyTest.
2. **Logging strategy:** Enhance the logging strategy to include file-based logging, improving the traceability and debugging of server-side errors.
3. **Response loading strategy:** Implement pagination for postcodes and suburbs, and explore alternative strategies (e.g., lazy loading) for optimizing data delivery in reporting features.
4. **Auth logic:** Refine the `token_required` decorator to efficiently return `signed_in_user` details, ensuring seamless authentication flows.

## Changelog

Date: 11/07/24

Updates:

1. Deployment: Deployed to Azure Web App
2. mySql DB: Created and seeded a new hosted cloud-based mysql db

Date: 12/07/24

Updates:

1. Addition of ProxyFix Middleware to solve the HTTPS redirecting to HTTP and causing a mixed content error on the front end: Since the deployment is on Azure Web App, which acts as a reverse proxy, it was necessary to integrate ProxyFix middleware. This middleware wraps the application to ensure Gunicorn correctly constructs the request based on the origin request's schema (HTTP/HTTPs). 

## Documentation

Explore the spring API documentation at: `https://postcheck-dgd3apheh6bdf0cw.australiaeast-01.azurewebsites.net/api/v1/docs`

<div align="center">
  <img src="./planning /Swagger_doc_new.png" style="max-width: 600px;" alt="Swagger documentation of PostCheck API">
</div>

## Technologies Used

<div align="center">

![Flask](https://img.shields.io/badge/-Flask-05122A?style=flat&logo=flask)
![MySQL](https://img.shields.io/badge/-MySQL-05122A?style=flat&logo=mysql)
![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-05122A?style=flat&logo=sqlalchemy)
![Flask-Smorest](https://img.shields.io/badge/-Flask%20Smorest-05122A?style=flat)
![Marshmallow](https://img.shields.io/badge/-Marshmallow-05122A?style=flat)
![Gunicorn](https://img.shields.io/badge/-Gunicorn-05122A?style=flat&logo=gunicorn)
![PyJWT](https://img.shields.io/badge/-PyJWT-05122A?style=flat)
![Docker](https://img.shields.io/badge/-Docker-05122A?style=flat&logo=docker)
![Git](https://img.shields.io/badge/-Git-05122A?style=flat&logo=git)
![GitHub](https://img.shields.io/badge/-GitHub-05122A?style=flat&logo=github)

</div>
