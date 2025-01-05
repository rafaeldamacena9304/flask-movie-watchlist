# Movie Watchlist App 🎬🍿

## Descrição do Projeto 🌟

Este projeto é uma **aplicação web** construída com o framework **Flask** que permite aos usuários criar uma lista de filmes para assistir, adicionar filmes, avaliá-los e visualizar detalhes sobre cada um. A aplicação armazena todos os dados em um banco de dados **MongoDB** na **Nuvem**, o que a torna flexível e escalável.

A ideia deste projeto foi criar uma plataforma simples, intuitiva e eficiente para demonstrar aqui meus conhecimentos do framework.

## Funcionalidades 🚀

### 📜 Funcionalidades Principais:

- **Exibição de Filmes**: Visualize uma lista de filmes disponíveis, com seus detalhes e informações básicas.
- **Cadastro e Login de Usuários**: Crie uma conta ou faça login para adicionar filmes e interagir com a lista.
- **Adicionar Filmes**: Usuários autenticados podem adicionar novos filmes ao banco de dados.
- **Avaliação de Filmes**: Avalie os filmes com uma nota de 1 a 5 estrelas.
- **Lista de Filmes Assistidos**: Adicione filmes à sua lista de filmes assistidos.
- **Exibição de Detalhes de Filmes**: Veja mais informações sobre cada filme, incluindo título, diretor, gênero e sinopse.

### 🧑‍🤝‍🧑 Recursos Sociais:
- **Usuários Únicos**: Cada usuário tem sua própria conta e lista de filmes assistidos.
- **Avaliação de Filmes**: Os usuários podem avaliar filmes e ver o total de avaliações de cada filme.

## Tecnologias Usadas 💻

- **Python 3.x**: A linguagem principal para o desenvolvimento da aplicação.
- **Flask**: Framework web usado para o desenvolvimento do backend.
- **MongoDB**: Banco de dados NoSQL utilizado para armazenar os dados dos filmes e dos usuários.
- **Jinja2**: Motor de templates do Flask para renderização de HTML dinâmico.
- **Passlib**: Biblioteca usada para hash de senhas dos usuários.
- **Bleach**: Ferramenta para limpar entradas de dados e proteger contra XSS.
- **UUID**: Utilizado para gerar identificadores únicos para os filmes e usuários.
- **HTML5/CSS3**: Para a criação das páginas web.

## Como o Projeto Funciona ⚙️

### Estrutura do Projeto:
1. **Banco de Dados MongoDB**: Os dados dos filmes e dos usuários são armazenados no MongoDB Cloud, com dados de cada filme, como título, diretor, gênero, descrição e avaliações. A URI do MongoDB é necessária para que a aplicação se conecte corretamente ao banco de dados.
2. **Autenticação de Usuários**: Usamos sessões Flask para garantir que apenas usuários autenticados possam adicionar filmes ou avaliá-los. 
3. **Avaliação de Filmes**: O sistema calcula a média de avaliação dos filmes com base nas avaliações de usuários. 
4. **Listas de Filmes**: Cada usuário tem uma lista personalizada de filmes que assistiu, facilitando o controle dos filmes que foram visualizados.

### Rotas Importantes:
- **/register**: Página para o usuário criar uma conta.
- **/login**: Página para o usuário realizar login na aplicação.
- **/index**: Página inicial que exibe todos os filmes disponíveis.
- **/add_movie**: Formulário para adicionar um novo filme (apenas para usuários autenticados).
- **/movie_details/<_id>**: Página de detalhes de um filme específico.
- **/rate_movie/<_id>**: Função para o usuário avaliar um filme.
- **/my_movies/<username>**: Página que exibe a lista de filmes assistidos pelo usuário.

## O que busquei agregar à comunidade 🌍

Este projeto tem como objetivo fornecer uma plataforma simples, mas funcional, para o controle de filmes assistidos, e ao mesmo tempo, demonstrar como construir uma aplicação com **Flask** e **MongoDB**. Além disso, ao usar **MongoDB Cloud**, o projeto é facilmente escalável e pode ser adaptado para diferentes necessidades no futuro.

Se você é iniciante em Flask ou MongoDB, este projeto pode ser uma excelente forma de aprender como integrar essas tecnologias de maneira eficiente.

## Instalação e Execução 🔧

1. **Clone o repositório**:

    ```bash
    git clone https://github.com/seu-usuario/movie-watchlist-app.git
    ```

2. **Instale as dependências**:

    Se você ainda não tem o **virtualenv** instalado, instale com:

    ```bash
    pip install virtualenv
    ```

    Crie e ative o ambiente virtual:

    ```bash
    virtualenv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

    Agora, instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure o MongoDB**:
    - Crie uma conta no [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (caso ainda não tenha).
    - Crie um novo cluster e obtenha a URI de conexão com o banco de dados.
    - Altere a URI de conexão no código (geralmente no arquivo de configuração do banco de dados).

4. **Execute a aplicação**:

    ```bash
    python run.py
    ```

5. Abra o navegador e acesse `http://127.0.0.1:5000`.

---

✨ **Aproveite o projeto e divirta-se assistindo seus filmes!** 🎥
