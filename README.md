
# med-appointments

A REST API service to manage medical appointments of a large hospital.

- Django
- Django REST Framework
- JWT Authentication

#### Signup an user

```http
  POST /api/signup/
```

| Parameters      |   Type     | Description                        |
| :----------     | :-------   | :----------------------            |
| `cpf`           |`STRING`|    **Required**. Customers's CPF       | 
|  `password`     |`STRING`|    **Required**. Customers's password  |
|  `nome`     |`STRING`|        **Required**. Customers's name      |
|  `nome_social`     |`STRING`| **Required**. Customers's social name|
|  `cns`     |`INT`|         **Required**. Customers's CNS                |
|  `uf`     |`STRING`|          **Required**. Customers's uf                  |
|  `cidade`     |`STRING`      |**Required**. Customers's city            |
|  `bairro`     |`STRING`      |**Required**. Customers's district        |
|  `complemento`     |`STRING`| **Required**. Customers's complement |
|  `cep`     |`STRING`|         **Required**. Customers's CEP                |

#### Login an user

```http
  POST /api/login/
```

| Parameters      |   Type     | Description                        |
| :----------     | :-------   | :----------------------            |
| `cpf`           |`STRING`|    **Required**. Customers's CPF       | 
|  `password`     |`STRING`|    **Required**. Customers's password  |

#### Create a queue
```http
  POST /api/queue/
```

| Parameters      |   Type     | Description                        |
| :----------     | :-------   | :----------------------            |
| `nome_fila`           |`STRING`|    **Required**. Queue's name       | 
|  `especialidade`     |`STRING`|    **Required**. Queue's specification |

#### Delete a queue
```http
  DELETE /api/queue/
```

| Parameters      |   Type     | Description                        |
| :----------     | :-------   | :----------------------            |
| `nome_fila`           |`STRING`|    **Required**. Queue's name       | 
|  `especialidade`     |`STRING`|    **Required**. Queue's specification |

#### Update a queue
```http
  PUT /api/queue/
```

| Parameters      |   Type     | Description                        |
| :----------     | :-------   | :----------------------            |
| `nome_fila`           |`STRING`|    **Required**. Queue's name       | 
|  `especialidade`     |`STRING`|    **Required**. Queue's specification |
| `novo_medico`           |`STRING`|    **Required**. Queue's new doctor       | 
|  `nova_especialidade`     |`STRING`|    **Required**. Queue's new specification |

#### Create an appointment
```http
  POST /api/consulta/user/
```

| Headers     | Description                           |
| :---------- | :---------------------------------- |
| `Authorization` | **Required**. Token JWT|

| Parameters      |   Type     | Description                        |
| :----------     | :-------   | :----------------------            |
| `nome_fila`           |`STRING`| **Required**. Queue's name       | 
|  `especialidade`     |`STRING`| **Required**. Queue's specification |
| `descricao`           |`STRING`| **Required**. Queue's description      | 
| `preferencia`           |`STRING`| **Required**. Queue's preference      | 
|  `data_prevista`     |`STRING`| Queue's expected date |
|  `data_conclusao`     |`STRING`| Appointment's conclusion date |

#### Delete an appointment
```http
  DELETE /api/consulta/user/
```
| Headers     | Description                           |
| :---------- | :---------------------------------- |
| `Authorization` | **Required**. Token JWT |

| Parameters      |   Type     | Description                        |
| :----------     | :-------   | :----------------------            |
| `nome_fila`           |`STRING`| **Required**. Queue's name       | 
|  `especialidade`     |`STRING`| **Required**. Queue's specification |

#### Update an appointment
```http
  PUT /api/consulta/user/
```

| Headers     | Description                           |
| :---------- | :---------------------------------- |
| `Authorization` | **Required**. Token JWT |

| Parameters      |   Type     | Description                        |
| :----------     | :-------   | :----------------------            |
| `novo_medico`           |`STRING`| **Required**. Queue's new name       | 
|  `nova_especialidade`     |`STRING`| **Required**. Queue's specification |
| `descricao`           |`STRING`| Queue's description       |
| `preferencia`           |`STRING`| Queue's preference      | 
|  `data_prevista`     |`STRING`| Appointment's expected date |
|  `data_conclusao`     |`STRING`| Appointment's conclusion date |

#### Delete an user
```http
  DELETE /api/user/
```

| Headers     | Description                           |
| :---------- | :---------------------------------- |
| `Authorization` | **Required**. Token JWT |

#### Update an user
```http
  PUT /api/user/
```

| Headers     | Description                           |
| :---------- | :---------------------------------- |
| `Authorization` | **Required**. Token JWT |

| Parameters      |   Type     | Description                        |
| :----------     | :-------   | :----------------------            |
|  `password`     |`STRING`|    **Required**. Customers's password  |
|  `nome`     |`STRING`|        **Required**. Customers's name      |
|  `nome_social`     |`STRING`| **Required**. Customers's social name|
|  `cns`     |`INT`|         **Required**. Customers's CNS                |
|  `uf`     |`STRING`|          **Required**. Customers's uf                  |
|  `cidade`     |`STRING`      |**Required**. Customers's city            |
|  `bairro`     |`STRING`      |**Required**. Customers's district        |
|  `complemento`     |`STRING`| **Required**. Customers's complement |
|  `cep`     |`STRING`|         **Required**. Customers's CEP                |
