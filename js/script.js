let menuIcon = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menuIcon.onclick = () => {
    menuIcon.classList.toggle('bx-x');
    navbar.classList.toggle('active');
}

const campoCep = document.getElementById('cep');
const botaoCep = document.getElementById('btn-buscar-cep');
const mensagem = document.getElementById('mensagem');

function mostrarMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.className = 'mensagem ' + tipo; // tipo: "erro", "sucesso" ou "carregando"
}

function limparEndereco() {
    ['rua', 'bairro', 'cidade', 'uf'].forEach(id => {
        document.getElementById(id).value = '';
    });
}

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

function iniciarBusca() {
    const cep = campoCep.value.replace(/\D/g, ''); // deixa só os números

    if (cep.length !== 8) {
        limparEndereco();
        mostrarMensagem('Digite um CEP com 8 números.', 'erro');
        return;
    }
    buscarCEP(cep);
}

if (campoCep) {
    botaoCep.addEventListener('click', iniciarBusca);
    campoCep.addEventListener('blur', () => {
        if (campoCep.value.trim() !== '') iniciarBusca();
    });
}