GQM
characteristics
Subcharacteristics:
Measures
Metrics


## Endpoints que retorna o catálogo de entidades suportadas pelo sistema atualmente

#### Lista todas as métricas conhecidas pelo repositório
/api/v1/metrics/

#### Lista todas as medidas suportadas pelo repositório
/api/v1/measures/

#### Lista todas as subcharacteristics suportadas pelo repositório
/api/v1/subcharacteristics/

#### Lista todas as characteristics suportadas pelo repositório
/api/v1/characteristics/




## Endpoints que cadastram ou solicitam o cálculo de uma entidade

#### Registra uma nova **métrica** em um repositório
/api/v1/orgs/1/repositories/1/create/metrics/

#### Endpoint que salva todas as métricas contidas no json do sonarqube
/api/v1/orgs/1/repositories/1/create/metrics/sonarqube/

#### Endpoint que salva todas as métricas contidas no json do github
/api/v1/orgs/1/repositories/1/create/metrics/github/

#### Calcula e retorna o valor atual de uma **medida** em um repositório
/api/v1/orgs/1/repositories/1/calculate/measures/1/

#### Calcula e retorna o valor atual de uma **subcharacteristics** em um repositório
/api/v1/orgs/1/repositories/1/calculate/subcharacteristics/1/

#### Calcula e retorna o valor atual de uma **characteristics** em um repositório
/api/v1/orgs/1/repositories/1/calculate/characteristics/1/

#### Calcula e retorna o valor atual do **gqm** do repositório
/api/v1/orgs/1/repositories/1/create/gqm/

















## Endpoints para leitura de dados já calculados/cadastrados (READ-ONLY)

### Métrics

#### Endpoint que retorna uma lista com o valor atual de todas as métricas associadas com um projeto
/api/v1/orgs/1/repositories/1/metrics/

#### Endpoint que retorna o valor atual de uma métrica associada a um projeto
/api/v1/orgs/1/repositories/1/metrics/1/

#### Endpoint que retorna uma lista com o histórico de valores de uma métrica de um projeto
/api/v1/orgs/1/repositories/1/metrics/1/history/

#### Endpoint que retorna o valor atual das metrics e de seus componentes
/api/v1/orgs/1/repositories/1/metrics/tree/

#### Endpoint que retorna o valor atual de uma metric e de seus componentes
/api/v1/orgs/1/repositories/1/metrics/1/tree/


### Medidas

#### Endpoint que retorna uma lista com o valor atual de todas as medidas associadas com um projeto
/api/v1/orgs/1/repositories/1/measures/

#### Endpoint que retorna o valor atual de uma medida associada a um projeto
/api/v1/orgs/1/repositories/1/measures/1/

#### Endpoint que retorna uma lista com o histórico de valores de uma medida de um projeto
/api/v1/orgs/1/repositories/1/measures/1/history/

#### Endpoint que retorna o valor atual das measures e de seus componentes
/api/v1/orgs/1/repositories/1/measures/tree/

#### Endpoint que retorna o valor atual de uma measure e de seus componentes
/api/v1/orgs/1/repositories/1/measures/1/tree/


### subcharacteristics

#### Endpoint que retorna uma lista com o valor atual de todas as subcharacteristics associadas com um projeto
/api/v1/orgs/1/repositories/1/subcharacteristics/

#### Endpoint que retorna o valor atual de uma subcharacteristic associada a um projeto
/api/v1/orgs/1/repositories/1/subcharacteristics/1/

#### Endpoint que retorna uma lista com o histórico de valores de uma subcharacteristic de um projeto
/api/v1/orgs/1/repositories/1/subcharacteristics/1/history/

#### Endpoint que retorna o valor atual das subcharacteristics e de seus componentes
/api/v1/orgs/1/repositories/1/subcharacteristics/tree/

#### Endpoint que retorna o valor atual da subcharacteristic e de seus componentes
/api/v1/orgs/1/repositories/1/subcharacteristics/1/tree/


### characteristics

#### Endpoint que retorna uma lista com o valor atual de todas as characteristics associadas com um projeto
/api/v1/orgs/1/repositories/1/characteristics/

#### Endpoint que retorna o valor atual de uma characteristic associada a um projeto
/api/v1/orgs/1/repositories/1/characteristics/1/

#### Endpoint que retorna uma lista com o histórico de valores de uma characteristic de um projeto
/api/v1/orgs/1/repositories/1/characteristics/1/history/

#### Endpoint que retorna o valor atual das characteristics e de seus componentes
/api/v1/orgs/1/repositories/1/characteristics/tree/

#### Endpoint que retorna o valor atual da characteristic e de seus componentes
/api/v1/orgs/1/repositories/1/characteristics/1/tree/


### gqm

#### Endpoint que retorna o valor atual do gqm de um projeto
/api/v1/orgs/1/repositories/1/gqm/

#### Endpoint que retorna o histórico do gqm de um projeto
/api/v1/orgs/1/repositories/1/gqm/history


#### Endpoint que retorna o valor atual do gqm e de seus componentes
/api/v1/orgs/1/repositories/1/gqm/tree/