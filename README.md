Helena Kunz Aires

Instituto de Informática e Estatística

Universidade Federal de Santa Catarina

07/11/2020

# Informações Gerais
- Linguagem: Python
- Estruturas de dados utilizadas:
	- Lista, Set, Dicionário: nativas da linguagem
	- Árvore: [treelib](https://treelib.readthedocs.io/en/latest/)
- Bibliotecas auxiliares:
	- [treelib](https://treelib.readthedocs.io/en/latest/)
	- [simple-term-menu](https://pypi.org/project/simple-term-menu/)
- Repositório: [github](https://github.com/lkaires/ine5421-implementacao)

# Detalhes de implementação
- O salvamento de arquivos usa json, passando a estrutura (um dicionário) para
  string. Os arquivos vão para a pasta .save, dentro da pasta do projeto.
- Existem 5 arquivos fonte:
	- `\_\_init\_\_.py`: Possui a lógica dos menus;
	- `io\_terminal.py`: Possui a parte de entrada e saída e parte da
	  lógica de input;
	- `automata.py`: Possui todas as funções que são chamadas pelo menu de
	  autômatos, ou seja, todas as funções que pedem um autômato como
parâmetro. Também possui parte da lógica de input de autômatos;
	- `grammar.py`: No momento possui apenas parte da lógica de input de
	  gramáticas;
	- `expression.py`: Possui parte da lógica de input de expressões, a
	  conversão de ER para AFD e a criação (não-funcional) de árvores de
sintaxe.
- Algumas coisas pedidas na entrega não foram implementadas:
	- edição de estruturas;
	- conversão de AFD para GR;
	- conversão de GR para AFND;
	- conversão de ER para AFD.
- A conversão de ER para AFD foi parcialmente implementada, porém ainda não
  funciona. O problema atualmente está na árvore de sintaxe, o algoritmo da
conversão em si a princípio funciona corretamente.

# Execução
- Para executar, é preciso baixar as bibliotecas auxiliares (seguindo os guias de instalação de cada uma);
- Depois de baixadas as bibliotecas, bastar rodar

```
python manip/__init__.py
```
