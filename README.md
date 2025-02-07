# Sistema de Gerenciamento de Estoque

## Visão Geral

Este sistema foi desenvolvido para agilizar o processo de vendas, facilitando o gerenciamento de estoque, localização de produtos e integração com impressoras e sistemas de envio.

## Módulos

### Acervo e Acervo\_Superior

Esses módulos contêm basicamente o mesmo sistema, com algumas diferenças específicas. Eles são necessários apenas se houver mais de um acervo físico em locais distintos.

### Mapeamento

Este módulo exibe a localização exata do produto dentro do estoque. Para isso, é necessário realizar o **range de mapeamento**. Caso contrário, o sistema exibirá apenas a numeração do produto, tornando a busca mais demorada.

### Elgin

Responsável pela geração de códigos de barras e integração com impressoras. Por padrão, está configurado para impressoras térmicas.

### Envia

Sistema de envio via e-mail. Permite a verificação automática de produtos na lista de vendas recebida via callback, possibilitando a integração com o checkout e reduzindo erros no processo de envio.

## Gestão de sequência dos Produtos

Ao remover um produto, o sistema armazena sua numeração e prioriza esse número ao registrar um novo produto. Dessa forma, a sequência numérica é mantida sem buracos, garantindo uma organização eficiente do estoque.

## Telas do Sistema

### Tela de Entrada de Dados
![Tela de Entrada](assets/tela_entrada.png)

### Tela de Saída de Dados
![Tela de Saída](assets/tela_saida.png)

