// Seleciona os elementos do menu mobile
let menuIcon = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

// Abre/fecha o menu ao clicar no ícone
menuIcon.onclick = () => {
    menuIcon.classList.toggle('bx-x');
    navbar.classList.toggle('active');
}

// Busca os campos de CEP e os elementos da mensagem
const campoCep = document.getElementById('cep');
const botaoCep = document.getElementById('btn-buscar-cep');
const mensagem = document.getElementById('mensagem');

// Mostra mensagens de status como carregando, erro ou sucesso
function mostrarMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.className = 'mensagem ' + tipo; // tipo: "erro", "sucesso" ou "carregando"
}

// Limpa os campos de endereço antes de preencher novamente
function limparEndereco() {
    ['rua', 'bairro', 'cidade', 'uf'].forEach(id => {
        document.getElementById(id).value = '';
    });
}

// Busca o endereço completo usando a API do ViaCEP
async function buscarCEP(cep) {
    try {
        mostrarMensagem('Buscando CEP...', 'carregando');
        botaoCep.disabled = true;

        const resposta = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
        if (!resposta.ok) throw new Error('Falha na requisição');

        const dados = await resposta.json();

        // O ViaCEP responde 200 com {"erro": true} quando o CEP não existe
        if (dados.erro) {
            limparEndereco();
            mostrarMensagem('CEP não encontrado. Confira os números e tente de novo.', 'erro');
            return;
        }

        // Preenche os campos do endereço com os dados retornados pela API
        document.getElementById('rua').value = dados.logradouro;
        document.getElementById('bairro').value = dados.bairro;
        document.getElementById('cidade').value = dados.localidade;
        document.getElementById('uf').value = dados.uf;
        mostrarMensagem('Endereço preenchido com sucesso!', 'sucesso');
    } catch (erro) {
        console.error('Falha ao buscar o CEP:', erro);
        limparEndereco();
        mostrarMensagem('Não foi possível buscar o CEP agora. Verifique sua conexão e tente novamente.', 'erro');
    } finally {
        botaoCep.disabled = false;
    }
}

// Valida e inicia a busca do CEP digitado pelo usuário
function iniciarBusca() {
    const cep = campoCep.value.replace(/\D/g, ''); // deixa só os números

    if (cep.length !== 8) {
        limparEndereco();
        mostrarMensagem('Digite um CEP com 8 números.', 'erro');
        return;
    }
    buscarCEP(cep);
}

// Dispara a busca ao clicar no botão ou ao sair do campo de CEP
if (campoCep) {
    botaoCep.addEventListener('click', iniciarBusca);
    campoCep.addEventListener('blur', () => {
        if (campoCep.value.trim() !== '') iniciarBusca();
    });
}

// URL da API local do backend
const API = "http://127.0.0.1:5000";

// Busca os projetos na API backend e exibe no console
async function carregarProjetos() {
    try {
        const resposta = await fetch(`${API}/projetos`);

        if (!resposta.ok) {
            throw new Error("Erro ao buscar projetos");
        }

        const projetos = await resposta.json();

        console.log(projetos);

    } catch (erro) {
        console.error("Erro:", erro);
    }
}

// Chama a função ao carregar a página
carregarProjetos();

const lista = document.getElementById("lista-projetos");

lista.innerHTML = "";

projetos.forEach(projeto => {
    const card = document.createElement("div");

    card.classList.add("service-box");

    card.innerHTML = `
        <div class="service-info">
            <h4>${projeto.titulo}</h4>
            <p>${projeto.descricao}</p>
        </div>
    `;

    lista.appendChild(card);
});
