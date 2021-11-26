# Libraries
import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px


# Hackathon dashboard

# Changing the page layout

# -- Set page config
apptitle = 'Dermatite atópica'
st.set_page_config(layout="wide")


#  Magic command to cache data
@st.cache(allow_output_mutation=True)
def get_data(filename):
    """load dataframes"""
    dataframe = pd.read_csv(filename)
    return dataframe


# Introduction container
introduction = st.container()

with introduction:
    st.image('https://mokshaderm.com/wp-content/uploads/2021/08/derm1.jpg', use_column_width=True)
    st.title('Dermatite atópica')
    st.markdown(
        '###### A dermatite atópica (DA) é uma doença crônica que se manifesta em crianças, mas que pode persistir até a adolescência. A DA tem 3 formas de apresentação: leve, moderada e grave. Quando a DA está na forma grave, necessita de internação. Segundo o IBGE há  aproximadamente um universo de 27 milhões de crianças de até 9 anos no Brasil. Vários trabalhos mostram que a prevalência da doença pode chegar até 12%, assim, calcula-se que um número enorme de possíveis pacientes podem ter DA. Atualmente o sistema único de saúde (SUS) não disponibiliza o tratamento  ideal  aos pacientes com DA, tratamento este já disponível na assistência médica privada. A disponibilização do tratamento mais adequada aos pacientes do sistema público de saúde permitirá melhor controle da doença, evitando internações e diminuindo o impacto da DA na sociedade.')

first_question = st.container()
with first_question:
    st.subheader(
        'Qual o custo anual médio dos pacientes com dermatite atópica moderada a grave para o sistema público de saúde?')
    #custos = get_data('data/summary.csv')
    custos = get_data('https://raw.githubusercontent.com/suebatista/streamlit_dermatitis/main/hackathon/data/summary.csv')

graph, blank, indicator = st.columns(3)

with graph:
    fig = px.bar(custos.reset_index(), x='ANO', y='VALOR', color='SEVERIDADE',
                 title='Custo total por tipo de severidade')
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                       'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                       })

    st.write(fig)
with st.expander("Veja explicação"):
    st.markdown("""
    **DEFINIÇÃO DE SEVERIDADE**

De acordo com a análise exploratória das bases de dados SIA (Produção Ambulatorial) e SIH (Internações Hospitalares) realizada nesse notebook, considerando que:

1. Dos medicamentos mencionados pela apresentação 'Datathon Abbvie - Análise das bases' fornecida pelo time Eretz.bio, apenas a **Ciclosporina** foi encontrada nas bases de dados em registros (**97 registros provenientes de BPA-I**) que tinham o CID10 L20, Dermatite Atópica, como causa principal ou causas secundárias;
2. Não foram encontrados registros de tratamentos de **Fototerapia ou Fototerapia com sensibilização** realizados para o CID10 L20 como causa principal e/ ou causas secundárias;
3. Não foram encontrados registros de **corticosteróides ou inibidores de calcineurina** dispensados para o CID10 L20 como causa principal e/ou causas secundárias, o que impede uma clara divisão entre casos Leves e Moderados de DA.


Optamos por classificar os casos de Dermatite Atópica da seguinte forma:

| Severidade | Definição baseada no histórico de tratamento entre 2016 e 2020 |
| -------------------------- | ----------------------- |
| GRAVE | - Pacientes que foram internados (AIH) pelo menos uma vez no período |
|  | - Pacientes que receberam ciclosporina |
|  | - Pacientes que usaram algum estabelecimento de saúde do tipo Emergência (ex.: Pronto Atendimentos |
|  | - Pacientes que receberam algum procedimento de Emergência |
|  | - Pacientes que geraram registros de APAC |
| LEVE/MODERADO | - Qualquer paciente que não se enquadrou em nenhum dos critérios considerados graves |
__________________________________________________________________________________________________________


  Como as bases de dados são públicas e não há nenhum campo que identifica cada paciente de maneira única, optamos por criar uma chave de identificação artificial através da concatenação dos campos de Município + Ano de Nascimento + Sexo. Apesar de imperfeito, considerando que apenas 0,87% de todos os registros ambulatoriais doenças de pele (CID10 capítulo XII), essa abordagem parece ser a que faz mais sentido e a que possibilita manter um controle, ainda que limitado, da progressão dos pacientes ao longo do tempo.

  Para responder essa pergunta, as bases principais (SIA e SIH) foram concatenadas para oferecer um visão total dos valores e outras estatísticas.

Além disso, foram considerados apenas os registros de L20 como causa primária. No caso de atendimentos ambulatoriais (SIA), os custos relacionados a registros de L20 como causa secundária são irrelevantes. No caso de internações hospitalares, os valores de registros com L20 como causa secundária ultrapassam a média de R$ 123.000,00 por ano. No entanto, não parece correto considerar esse valores, uma vez que as causas primárias são as mais variadas (asma, pneumonia, celulite, infecções diversas, bronquiolite, etc) e apesar de poder existir relação entre a dermatite atópica e essas outras enfermidades, a causa primária de internação não foi a dermatite.    """)

with blank:
    st.write('-')

with indicator:
    indicator.metric("Custo anual médio por ano", "R$413.341,8")
    indicator.metric("O ano com o maior custo foi", "2019")

second_question = st.container()
with second_question:
    st.subheader("Como se caracteriza a utilização de recursos do sistema de saúde por pacientes com dermatite "
                 "atópica moderada a grave?")

graph2, blank2, indicator2 = st.columns(3)

with graph2:
    second_question = get_data('https://raw.githubusercontent.com/suebatista/streamlit_dermatitis/main/hackathon/data/pacientes_ano.csv')
    fig2 = px.bar(second_question.reset_index(), x='ANO', y='PACIENTES',
                  title='Pacientes com CID L20 atendidos por ano')
    fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                        })

    st.write(fig2)

with blank2:
    st.write('-')

with indicator2:
    third_question = get_data('https://raw.githubusercontent.com/suebatista/streamlit_dermatitis/main/hackathon/data/tipo_atendimento.csv')
    fig3 = px.bar(third_question.reset_index(), x='ANO', y='PACIENTES', color='TIPO_ATENDIMENTO',
                  title='Quantos pacientes atendidos em serviços de emergência? E quantos são ambulatoriais?')
    fig3.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                        })

    st.write(fig3)

graph3, indicator3 = st.columns(2)
with graph3:
    # st.header('Como se caracteriza a utilização de recursos do sistema de saúde por pacientes com dermatite atópica moderada a grave?')
    internacoes = get_data('https://raw.githubusercontent.com/suebatista/streamlit_dermatitis/main/hackathon/data/internacao_custos.csv')
    internacoes = px.bar(internacoes.reset_index(), x='FAIXA_ETARIA', y='NUM_PROCEDIMENTOS',
                         title='Quantidade de internações por faixa etária')
    internacoes.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                               'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                               })
    st.write(internacoes)
with indicator3:
    pergunta4 = get_data('https://raw.githubusercontent.com/suebatista/streamlit_dermatitis/main/hackathon/data/age_groups.csv')
    st.write('-')
    st.write('Quantidade de tipo de atendimento por faixa etária')

    option = st.selectbox('Escolha uma faixa etária',
                          ('0-6', '6-12', '12-18', '18-30', '30-50', '50+'))
    df = pergunta4[pergunta4['FAIXA_ETARIA'] == option]
    st.dataframe(df)

graph4, blank4, indicator4 = st.columns(3)

with graph4:
    tempo_internacao = get_data('https://raw.githubusercontent.com/suebatista/streamlit_dermatitis/main/hackathon/data/tempo_internacao.csv')
    tempo_internacao = px.bar(tempo_internacao.reset_index(), x='ANO_CMPT', y='MEDIA_DIAS_INTERNACAO',
                              title='Qual o tempo médio de dias de internação de pacientes com CID L20?',
                              labels={'ANO_CMPT': 'ANO'})
    tempo_internacao.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                    })
    st.write(tempo_internacao)

with blank4:
    st.write('-')

with indicator4:
    map = get_data('https://raw.githubusercontent.com/suebatista/streamlit_dermatitis/main/hackathon/data/mapa.csv')
    map = px.scatter_mapbox(map.reset_index(),
                            lat='NU_LATITUDE',
                            lon='NU_LONGITUDE',
                            color='SEVERIDADE',
                            size='NUM_PACIENTES',
                            size_max=20,
                            zoom=2.5,
                            mapbox_style='open-street-map',
                            title='Concentração de casos de Dermatite Atópica por localidade')
    st.write(map)

with st.expander("Veja explicação"):
    st.markdown("""
  A consulta de quantos pacientes atendidos por ano retorna a quantidade de pacientes únicos atendidos por ano. Isso quer dizer que o mesmo paciente pode ter sido atendido uma ou mais vezes.


  Para análise do número de consultas ambulatoriais e emergenciais por paciente por mês, assumimos que cada registro de BPA-I na tabela SIA de produção ambulatorial representa um atendimento ou consulta. O informe técnico 2016-03 SIASUS declara que "*há casos de registros de um ou mais atendimentos no BPA-I para o mesmo paciente*", mas é impossível identificar esses casos e serão considerados exceção. Como os campos de data da tabela não registram o dia dos atendimentos (apenas ano/mês, não é possível controlar artificialmente essa questão.    """)

third_question = st.container()
with third_question:
    st.subheader(
        'Qual a relação dos custos indiretos (licença médica, aposentadora precoce, DALY, etc) dos pacientes com dermatite atópica moderada a grave e seus cuidadores, comparando a outras doenças dermatológicas?')

graph6, blank6, indicator6 = st.columns(3)

with graph6:
    beneficios_doenca = get_data('https://raw.githubusercontent.com/suebatista/streamlit_dermatitis/main/hackathon/data/beneficios_doenca.csv')
    beneficios_doenca = px.bar(beneficios_doenca.reset_index(), x='ANO', y='NUM_BENEFICIOS', color='CID_SHORT',
                               title='Quantos benefícios solicitados e concedidos comparativamente entre as doenças?',
                               barmode='group')
    beneficios_doenca.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                     'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                     })
    st.write(beneficios_doenca)

with blank6:
    st.write('-')

with indicator6:
    beneficios_idade = get_data('https://raw.githubusercontent.com/suebatista/streamlit_dermatitis/main/hackathon/data/beneficios_idade.csv')
    graph_beneficios_age = px.bar(beneficios_idade.reset_index(), x='CID_SHORT', y='NUM_BENEFICIOS',
                                  color='FAIXA_ETARIA',
                                  title='Qual a faixa etária que mais solicita benefícios em cada uma das doenças?',
                                  barmode="group", labels={'CID_SHORT': "CID"
                                                           })
    graph_beneficios_age.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                        })
    st.write(graph_beneficios_age)

graph7, blank7, indicator7 = st.columns(3)

with graph7:
    beneficios_tipo = get_data('https://raw.githubusercontent.com/suebatista/streamlit_dermatitis/main/hackathon/data/beneficios_tipos.csv')
    graph_beneficios_tipo = px.bar(beneficios_tipo.reset_index(), x='CID_SHORT', y='NUM_BENEFICIOS', color='Espécie',
                                   barmode='group',
                                   title='Quais tipos de benefícios mais solicitados e mais concedidos?')
    graph_beneficios_tipo.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                         'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                         })

    st.write(graph_beneficios_tipo)

with blank7:
    st.write('-')

with indicator7:
    df_daly = get_data('https://raw.githubusercontent.com/suebatista/streamlit_dermatitis/main/hackathon/data/df_daly.csv')
    df_daly = px.bar(df_daly.reset_index(), x='ANO', y='DALY', title='Qual seria o DALY para dermatite atópica?')
    df_daly.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                           'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                           })

    st.write(df_daly)

with st.expander("Veja explicação"):
    st.write("""
   DISABILITY ADJUSTED LIFE YEARS ou DALY

DALY = MORBIDITY + MORTALITY ou
DALY = YLD + YLL, onde:
YLD = Years Lived with Disability
YLL = Years of Life Lost

YLD = DW x P, onde:
DW = disability weight of the condition
P = prevalent cases in the population (de acordo com o último relatório técnico da OMS)

YLL = N x L, onde:
N = number of deaths due to condition
L = standard life expectancy at the age of death

Disability Weights retirados de 'Global Health Data Exchange' em http://ghdx.healthdata.org/record/ihme-data/gbd-2019-disability-weights


   **É importante lembrar que esses valores de DALY são estimados uma vez que dependem da informação de prevalência de casos, que por sua vez dependem da chave única de identificação de paciente, que foi artificialmente introduzida nas bases de dados**

Outra observação interessante é que o *Global Burden of Disease Study 2019 (GBD 2019)* estima um **DALY de 737.092 para todas as doenças de pele no Brasil**. Se considerarmos que a nossa análise determina que a Dermatite Atópica representa 0,87% de todos os registros de produção ambulatorial do SUS referentes à doencas de pele, se aplicarmos essa proporção na estimativa do GBD 2019 (0,87% x 737.092), teríamos um DALY para Dermatite Atópica de **6.412**. Em termos de grandeza, esse resultado parece consistente com os números de DALY que calculamos nessa análise a partir dos dados abertos do SUS.  """)

final_container = st.container()

with final_container:
    st.subheader('Quer saber mais sobre dermatite atópica no Brasil?')
    st.markdown('Acesse o [repositório do estudo](https://github.com/suebatista/hackathon)')
    st.text('Oferecimento: Equipe DataDES')

