CREATE TABLE IF NOT EXISTS quarteis (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL UNIQUE,
    sigla TEXT NOT NULL UNIQUE,
    efetivo INTEGER NOT NULL,
    area REAL NOT NULL,
    grupo_tarifario TEXT NOT NULL,
    demanda_contratada REAL NOT NULL
);


CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    quartel_id INTEGER NOT NULL,
    access_level INTEGER NOT NULL,

    FOREIGN KEY (quartel_id) 
        REFERENCES quarteis(id)
);

CREATE TABLE IF NOT EXISTS despesas(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    quartel_id INTEGER NOT NULL,
    valor REAL NOT NULL,
    efetivo INTEGER NOT NULL,
    area REAL NOT NULL,
    data_fatura TEXT NOT NULL,
    contratada REAL NOT NULL,
    demanda REAL NOT NULL,
    efetiva REAL NOT NULL,
    reativa REAL NOT NULL,
    multa REAL DEFAULT 0,

    FOREIGN KEY (quartel_id) 
        REFERENCES quarteis(id)
);

CREATE TABLE IF NOT EXISTS geradores(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    quartel_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    tipo TEXT NOT NULL,

    FOREIGN KEY (quartel_id) 
        REFERENCES quarteis(id)
);

CREATE TABLE IF NOT EXISTS geracao(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    gerador_id INTEGER NOT NULL,
    efetiva REAL NOT NULL,
    reativa REAL NOT NULL,
    consumo REAL NOT NULL,
    data_uso TEXT NOT NULL,

    FOREIGN KEY (gerador_id) 
        REFERENCES geradores(id)
);

CREATE TABLE IF NOT EXISTS hierarquia(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    quartel_id INTEGER NOT NULL,
    
    FOREIGN KEY (quartel_id) 
        REFERENCES quarteis(id)
);


-- adciona a OM principal, nesse caso uma ficticia
INSERT INTO quarteis (name, sigla, efetivo, area, grupo_tarifario, demanda_contratada) VALUES("EB Energia", "EBE", 0, 0, "", 0);

-- inicia o povoamento do grafo
ALTER TABLE hierarquia ADD EBE INTEGER NOT NULL DEFAULT 0;

-- adciona o primeiro item ao grafo
INSERT INTO hierarquia (quartel_id) VALUES (1);
