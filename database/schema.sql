-- Arquivo: database/schema.sql

CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf_documento VARCHAR(14) NOT NULL UNIQUE,
    cnh VARCHAR(11) NOT NULL UNIQUE,
    telefone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE veiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(8) NOT NULL UNIQUE,
    modelo VARCHAR(255) NOT NULL,
    ano INT,
    cor VARCHAR(50),
    quilometragem INT,
    status ENUM('Disponível', 'Alugado', 'Em Manutenção') NOT NULL DEFAULT 'Disponível',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE pecas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_peca VARCHAR(255) NOT NULL,
    qtd_estoque INT NOT NULL DEFAULT 0,
    custo_unitario DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE locacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    veiculo_id INT NOT NULL,
    cliente_id INT NOT NULL,
    data_retirada DATETIME NOT NULL,
    data_devolucao DATETIME,
    valor_aluguel DECIMAL(10, 2),
    quilometragem_retirada INT,
    quilometragem_devolucao INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE manutencoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    veiculo_id INT NOT NULL,
    data_manutencao DATE NOT NULL,
    quilometragem_manutencao INT,
    custo_total DECIMAL(10, 2),
    descricao TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id)
);

CREATE TABLE manutencao_pecas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    manutencao_id INT NOT NULL,
    peca_id INT NOT NULL,
    quantidade_usada INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (manutencao_id) REFERENCES manutencoes(id),
    FOREIGN KEY (peca_id) REFERENCES pecas(id)
);