CREATE TABLE IF NOT EXISTS "cliente" (
  "idcliente" INTEGER NOT NULL,
  "nome" VARCHAR(50) NULL DEFAULT NULL,
  "endereco" VARCHAR(50) NULL DEFAULT NULL,
  "telefone" VARCHAR(10) NULL DEFAULT NULL,
  "cnpj" VARCHAR(14) NULL DEFAULT NULL,
  "cpf" VARCHAR(12) NULL DEFAULT NULL,
  "email" VARCHAR(50) NULL DEFAULT NULL,
  "tipo" VARCHAR(1) NULL DEFAULT NULL,
  PRIMARY KEY ("idcliente"))

CREATE TABLE IF NOT EXISTS "motorista" (
  "idmotorista" INTEGER NOT NULL,
  "nome" VARCHAR(45) NULL DEFAULT NULL,
  "telefone" VARCHAR(45) NULL DEFAULT NULL,
  "endereco" VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY ("idmotorista"))

CREATE TABLE IF NOT EXISTS "entrega" (
  "identrega" INTEGER NOT NULL,
  "turno" VARCHAR(1) NULL DEFAULT NULL,
  "datahora_retirada" TEXT NULL DEFAULT NULL,
  "datahora_entrega" TEXT NULL DEFAULT NULL,
  "motorista_idmotorista" INTEGER NOT NULL,
  PRIMARY KEY ("identrega", "motorista_idmotorista"),
  CONSTRAINT "fk_entrega_motorista1"
    FOREIGN KEY ("motorista_idmotorista")
    REFERENCES "motorista" ("idmotorista"))

CREATE TABLE IF NOT EXISTS "pedido" (
  "idpedido" INTEGER NOT NULL,
  "tipo_pagamento" VARCHAR(45) NULL DEFAULT NULL,
  "datahora" VARCHAR(45) NULL DEFAULT NULL,
  "cliente_idcliente" INTEGER NOT NULL,
  PRIMARY KEY ("idpedido", "cliente_idcliente"),
  CONSTRAINT "fk_pedido_cliente"
    FOREIGN KEY ("cliente_idcliente")
    REFERENCES "cliente" ("idcliente"))

CREATE TABLE IF NOT EXISTS "entrega_has_pedido" (
  "entrega_identrega" INTEGER NOT NULL,
  "entrega_motorista_idmotorista" INTEGER NOT NULL,
  "pedido_idpedido" INTEGER NOT NULL,
  "pedido_cliente_idcliente" INTEGER NOT NULL,
  PRIMARY KEY ("entrega_identrega", "entrega_motorista_idmotorista", "pedido_idpedido", "pedido_cliente_idcliente"),
  CONSTRAINT "fk_entrega_has_pedido_entrega1"
    FOREIGN KEY ("entrega_identrega" , "entrega_motorista_idmotorista")
    REFERENCES "entrega" ("identrega" , "motorista_idmotorista"),
  CONSTRAINT "fk_entrega_has_pedido_pedido1"
    FOREIGN KEY ("pedido_idpedido" , "pedido_cliente_idcliente")
    REFERENCES "pedido" ("idpedido" , "cliente_idcliente"))

CREATE TABLE IF NOT EXISTS "usuario" (
  "idusuario" INTEGER NOT NULL,
  "login" VARCHAR(45) NULL DEFAULT NULL,
  "senha" VARCHAR(45) NULL DEFAULT NULL,
  "email" VARCHAR(45) NULL DEFAULT NULL,
  "tipo" VARCHAR(1) NULL DEFAULT NULL,
  PRIMARY KEY ("idusuario"))