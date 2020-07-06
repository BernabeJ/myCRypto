CREATE TABLE "movimientos" (
	"id"	INTEGER NOT NULL,
	"date"	TEXT,
	"time"	TEXT,
	"from_currency"	INTEGER,
	"form_quantity"	REAL,
	"to_currency"	INTEGER,
	"to_quantity"	REAL,
	"precio_unitario"	REAL,
	PRIMARY KEY("id")
)

CREATE TABLE "cryptos" (
	"id"	INTEGER NOT NULL,
	"symbol"	TEXT,
	"name"	TEXT,
	PRIMARY KEY("id")
)