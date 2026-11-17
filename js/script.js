// Endereço da API Flask.
const API = window.PORTFOLIO_API_URL || "http://127.0.0.1:5000";

// Elementos usados em mais de uma página.
const menuIcon = document.querySelector('#menu-icon');
const navbar = document.querySelector('.navbar');
let tokenCSRF = "";

// Menu para dispositivos menores.
if (menuIcon && navbar) {
    menuIcon.onclick = () => {
        menuIcon.classList.toggle('bx-x');
        navbar.classList.toggle('active');
    };
}

// Faz requisições para a API.
async function requisicaoAPI(caminho, opcoes = {}) {
    const cabecalhos = { ...(opcoes.headers || {}) };

    if (opcoes.body) {
        cabecalhos["Content-Type"] = "application/json";
    }

    // O token é necessário apenas em métodos que alteram estado; GET não altera
    // dados e o login ainda não possui um token emitido.
    if (tokenCSRF && opcoes.method && opcoes.method !== "GET") {
        cabecalhos["X-CSRF-Token"] = tokenCSRF;
    }

    const resposta = await fetch(`${API}${caminho}`, {
        ...opcoes,
        headers: cabecalhos,
        // Inclui o cookie de sessão nas chamadas à API, mesmo quando frontend e
        // backend estão em origens diferentes.
        credentials: "include"
    });

    // Algumas respostas podem não conter JSON; nesse caso, a mensagem abaixo
    // usa o texto padrão ao tratar uma resposta HTTP de erro.
    const dados = await resposta.json().catch(() => ({}));

    if (!resposta.ok) {
        throw new Error(
            dados.mensagem || "Não foi possível concluir a solicitação."
        );
    }

    return dados;
}

// Exibe mensagens de retorno.
function mostrarStatus(elemento, texto, tipo = "") {
    if (!elemento) return;

    elemento.textContent = texto;
    elemento.className = `status-admin ${tipo}`;
}

// Consulta o ViaCEP.
const campoCep = document.getElementById('cep');
const botaoCep = document.getElementById('btn-buscar-cep');
const mensagemCep = document.getElementById('mensagem');

function limparEndereco() {
    ['rua', 'bairro', 'cidade', 'uf'].forEach(id => {
        const campo = document.getElementById(id);

        if (campo) {
            campo.value = '';
        }
    });
}

async function buscarCEP(cep) {
    try {
        mostrarStatus(mensagemCep, 'Buscando CEP...', 'carregando');

        // Evita disparos repetidos enquanto a consulta externa está em andamento.
        if (botaoCep) {
            botaoCep.disabled = true;
        }

        const resposta = await fetch(
            `https://viacep.com.br/ws/${cep}/json/`
        );

        if (!resposta.ok) {
            throw new Error('Falha na requisição');
        }

        const dados = await resposta.json();

        if (dados.erro) {
            limparEndereco();

            mostrarStatus(
                mensagemCep,
                'CEP não encontrado. Confira os números e tente novamente.',
                'erro'
            );

            return;
        }

        document.getElementById('rua').value =
            dados.logradouro || '';

        document.getElementById('bairro').value =
            dados.bairro || '';

        document.getElementById('cidade').value =
            dados.localidade || '';

        document.getElementById('uf').value =
            dados.uf || '';

        mostrarStatus(
            mensagemCep,
            'Endereço preenchido com sucesso!',
            'sucesso'
        );

    } catch (erro) {
        limparEndereco();

        mostrarStatus(
            mensagemCep,
            'Não foi possível buscar o CEP. Tente novamente.',
            'erro'
        );

    } finally {
        // Reabilita o controle tanto em sucesso quanto em erro da consulta.
        if (botaoCep) {
            botaoCep.disabled = false;
        }
    }
}

function iniciarBuscaCEP() {
    const cep = campoCep.value.replace(/\D/g, '');

    if (cep.length !== 8) {
        limparEndereco();

        mostrarStatus(
            mensagemCep,
            'Digite um CEP com 8 números.',
            'erro'
        );

        return;
    }

    buscarCEP(cep);
}

if (campoCep && botaoCep) {
    botaoCep.addEventListener('click', iniciarBuscaCEP);

    campoCep.addEventListener('blur', () => {
        if (campoCep.value.trim() !== '') {
            iniciarBuscaCEP();
        }
    });
}

// Carrega os projetos na página Serviços.
async function carregarProjetos() {
    const lista = document.getElementById('lista-projetos');

    if (!lista) return;

    lista.innerHTML = '';

    try {
        const projetos = await requisicaoAPI('/projetos');

        if (projetos.length === 0) {
            lista.textContent =
                'Nenhum projeto cadastrado no momento.';

            return;
        }

        projetos.forEach(projeto => {
            const card = document.createElement('div');
            card.className = 'service-box projeto-card';

            const conteudo = document.createElement('div');
            conteudo.className = 'service-info';

            const titulo = document.createElement('h4');
            // textContent insere os dados como texto, sem interpretar HTML vindo
            // da API como marcação dentro da página.
            titulo.textContent = projeto.titulo;

            const descricao = document.createElement('p');
            descricao.textContent = projeto.descricao;

            conteudo.append(titulo, descricao);

            if (projeto.imagem) {
                const imagem = document.createElement('img');

                imagem.src = projeto.imagem;
                imagem.alt = projeto.titulo;
                imagem.className = 'imagem-projeto';

                conteudo.prepend(imagem);
            }

            if (projeto.link) {
                const link = document.createElement('a');

                link.href = projeto.link;
                link.target = '_blank';
                link.rel = 'noopener noreferrer';
                link.textContent = 'Ver projeto';
                link.className = 'btn';

                conteudo.appendChild(link);
            }

            card.appendChild(conteudo);
            lista.appendChild(card);
        });

    } catch (erro) {
        lista.textContent =
            `Não foi possível carregar os projetos: ${erro.message}`;
    }
}

// Envia o formulário de contato para o Flask.
const formularioContato = document.querySelector('#form-contato');

if (formularioContato) {
    formularioContato.addEventListener('submit', async evento => {
        evento.preventDefault();

        const status = document.getElementById('mensagem');

        const dados = {
            nome: document.getElementById('nome').value.trim(),
            email: document.getElementById('email').value.trim(),
            texto: document.getElementById('texto').value.trim(),

            cep: {
                cep: document.getElementById('cep').value.replace(/\D/g, ''),
                rua: document.getElementById('rua').value,
                bairro: document.getElementById('bairro').value,
                cidade: document.getElementById('cidade').value,
                uf: document.getElementById('uf').value
            }
        };

        try {
            const resultado = await requisicaoAPI('/mensagens', {
                method: 'POST',
                body: JSON.stringify(dados)
            });

            mostrarStatus(
                status,
                resultado.mensagem,
                'sucesso'
            );

            formularioContato.reset();
            limparEndereco();

        } catch (erro) {
            mostrarStatus(status, erro.message, 'erro');
        }
    });
}

// Funções da área administrativa.
const formularioLogin = document.getElementById('form-login');
const painelAdmin = document.getElementById('painel-admin');
const formularioProjeto = document.getElementById('form-projeto');
const statusAdmin = document.getElementById('status-admin');

let idProjetoEdicao = null;

function mostrarPainel(autenticado) {
    if (formularioLogin) {
        formularioLogin.hidden = autenticado;
    }

    if (painelAdmin) {
        painelAdmin.hidden = !autenticado;
    }
}

// Carrega projetos e mensagens no painel administrativo.
async function carregarDadosAdmin() {
    const listaAdmin =
        document.getElementById('lista-admin-projetos');

    const listaMensagens =
        document.getElementById('lista-mensagens');

    if (listaAdmin) {
        listaAdmin.innerHTML = '';

        const projetos = await requisicaoAPI('/projetos');

        projetos.forEach(projeto => {
            const item = document.createElement('div');
            item.className = 'admin-item';

            const titulo = document.createElement('strong');
            titulo.textContent = projeto.titulo;

            const descricao = document.createElement('p');
            descricao.textContent = projeto.descricao;

            const editar = document.createElement('button');
            editar.type = 'button';
            editar.className = 'btn';
            editar.textContent = 'Editar';

            editar.addEventListener('click', () => {
                // Guarda o ID para que o envio do formulário saiba que deve
                // atualizar este registro em vez de criar um novo.
                idProjetoEdicao = projeto.id_projeto;

                document.getElementById('titulo-projeto').value =
                    projeto.titulo || '';

                document.getElementById('descricao-projeto').value =
                    projeto.descricao || '';

                document.getElementById('imagem-projeto').value =
                    projeto.imagem || '';

                document.getElementById('categoria-projeto').value =
                    projeto.categoria || '';

                document.getElementById('link-projeto').value =
                    projeto.link || '';

                document.getElementById(
                    'botao-salvar-projeto'
                ).textContent = 'Salvar alterações';
            });

            const excluir = document.createElement('button');
            excluir.type = 'button';
            excluir.className = 'btn btn-secundario';
            excluir.textContent = 'Excluir';

            excluir.addEventListener('click', async () => {
                // Exige confirmação antes de enviar uma operação irreversível.
                if (!confirm(
                    `Deseja excluir o projeto "${projeto.titulo}"?`
                )) {
                    return;
                }

                try {
                    await requisicaoAPI(
                        `/projetos/${projeto.id_projeto}`,
                        { method: 'DELETE' }
                    );

                    mostrarStatus(
                        statusAdmin,
                        'Projeto excluído com sucesso!',
                        'sucesso'
                    );

                    await carregarDadosAdmin();

                } catch (erro) {
                    mostrarStatus(
                        statusAdmin,
                        erro.message,
                        'erro'
                    );
                }
            });

            item.append(titulo, descricao, editar, excluir);
            listaAdmin.appendChild(item);
        });
    }

    if (listaMensagens) {
        listaMensagens.innerHTML = '';

        const mensagens = await requisicaoAPI('/mensagens');

        if (mensagens.length === 0) {
            listaMensagens.textContent =
                'Nenhuma mensagem recebida.';
        }

        mensagens.forEach(mensagem => {
            const item = document.createElement('div');
            item.className = 'admin-item';

            const titulo = document.createElement('strong');
            // Mantém os dados recebidos como texto; o conteúdo de uma mensagem
            // não deve ser interpretado como elementos HTML.
            titulo.textContent =
                `${mensagem.nome} — ${mensagem.email}`;

            const texto = document.createElement('p');
            texto.textContent = mensagem.texto;

            const endereco = document.createElement('p');
            const cep = mensagem.cep || {};

            endereco.textContent =
                `CEP: ${cep.cep || ''} | ${cep.rua || ''}, ` +
                `${cep.bairro || ''} - ${cep.cidade || ''}/${cep.uf || ''}`;

            item.append(titulo, texto, endereco);
            listaMensagens.appendChild(item);
        });
    }
}

// Login administrativo.
if (formularioLogin) {
    formularioLogin.addEventListener('submit', async evento => {
        evento.preventDefault();

        try {
            const senha =
                document.getElementById('senha-admin').value;

            const resultado = await requisicaoAPI('/admin/login', {
                method: 'POST',
                body: JSON.stringify({ senha })
            });

            tokenCSRF = resultado.csrf_token;

            mostrarPainel(true);

            mostrarStatus(
                statusAdmin,
                resultado.mensagem,
                'sucesso'
            );

            formularioLogin.reset();

            await carregarDadosAdmin();

        } catch (erro) {
            mostrarStatus(
                statusAdmin,
                erro.message,
                'erro'
            );
        }
    });

    // Verifica se já existe uma sessão administrativa.
    requisicaoAPI('/admin/status')
        .then(resultado => {
            tokenCSRF = resultado.csrf_token;

            mostrarPainel(true);

            carregarDadosAdmin().catch(erro => {
                mostrarStatus(statusAdmin, erro.message, 'erro');
            });
        })
        .catch(() => mostrarPainel(false));
}

// Cadastro e edição de projetos.
if (formularioProjeto) {
    formularioProjeto.addEventListener('submit', async evento => {
        evento.preventDefault();

        const dados = {
            titulo: document.getElementById('titulo-projeto').value.trim(),
            descricao: document.getElementById('descricao-projeto').value.trim(),
            imagem: document.getElementById('imagem-projeto').value.trim(),
            categoria: document.getElementById('categoria-projeto').value.trim(),
            link: document.getElementById('link-projeto').value.trim()
        };

        try {
            const caminho = idProjetoEdicao
                ? `/projetos/${idProjetoEdicao}`
                : '/projetos';

            // A presença de um ID indica edição; sem ID, o formulário cadastra
            // um novo projeto.
            const metodo = idProjetoEdicao ? 'PUT' : 'POST';

            const resultado = await requisicaoAPI(caminho, {
                method: metodo,
                body: JSON.stringify(dados)
            });

            mostrarStatus(
                statusAdmin,
                resultado.mensagem,
                'sucesso'
            );

            formularioProjeto.reset();
            idProjetoEdicao = null;

            document.getElementById(
                'botao-salvar-projeto'
            ).textContent = 'Cadastrar projeto';

            await carregarDadosAdmin();

        } catch (erro) {
            mostrarStatus(
                statusAdmin,
                erro.message,
                'erro'
            );
        }
    });
}

// Cancela a edição de um projeto.
const botaoCancelarEdicao =
    document.getElementById('cancelar-edicao');

if (botaoCancelarEdicao) {
    botaoCancelarEdicao.addEventListener('click', () => {
        formularioProjeto.reset();
        idProjetoEdicao = null;

        document.getElementById(
            'botao-salvar-projeto'
        ).textContent = 'Cadastrar projeto';
    });
}

// Encerra a sessão administrativa.
const botaoSair = document.getElementById('sair-admin');

if (botaoSair) {
    botaoSair.addEventListener('click', async () => {
        try {
            await requisicaoAPI('/admin/logout', {
                method: 'POST'
            });

            tokenCSRF = '';

            mostrarPainel(false);

            mostrarStatus(
                statusAdmin,
                'Você saiu da área administrativa.',
                'sucesso'
            );

        } catch (erro) {
            mostrarStatus(
                statusAdmin,
                erro.message,
                'erro'
            );
        }
    });
}

// Executa as funções correspondentes à página aberta.
carregarProjetos();