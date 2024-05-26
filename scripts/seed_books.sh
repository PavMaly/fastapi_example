#!/bin/bash

psql --set ON_ERROR_STOP=OFF -h localhost -U "app" -d "app"<<-EOSQL
-- Книги
  CREATE TABLE IF NOT EXISTS books(
    book_id INT generated always as identity (start 100001) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    publisher VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'in collection'
    );

  DELETE FROM books;
  ALTER SEQUENCE  books_book_id_seq  RESTART WITH 100001;

  INSERT INTO books (title, publisher, year) values
  -- 100001
  ('Программирование cloud native', 'Издательские решения', 2020),
  -- 100002
  ('Изучаем python', 'Питер', 2022),
  -- 100003
  ('Океан в конце дороги', 'АСТ', 2022),
  -- 100004
  ('Благие знамения', 'Эксмо', 2023),
  -- 100005
  ('Чапаев и Пустота', 'АСТ', 2023),
  -- 100006
  ('Generation П', 'Азбука', '2022'),
  -- 100007
  ('Детство', 'Эксмо', 2019),
  -- 100008
  ('В людях', 'Эксмо', 2020),
  -- 100009
  ('Мои университеты', 'Эксмо', 2021),
  -- 100010
  ('Правила устройства электроустановок. Все действующие разделы ПУЭ-6 и ПУЭ-7', 'Норматика', 2020),
  -- 100011
  ('СП 52.13330.2016. Свод правил. Естественное и искусственное освещение (Актуализированная редакция СНиП 23-05-95*)', 'УралЮрИздат', 2021),
  -- 100012
  ('Статистика и котики', 'АСТ', 2022),
  -- 100013
  ('Скандинавские боги', 'АСТ', 2019),
  -- 100014
  ('Американские боги', 'АСТ', 2018),
  -- 100015
  ('Для программистов. Assembler для DOS, Windows и Unix', 'ДМК Пресс', 2017),
  -- 100016
  ('Высоконагруженные приложения. Программирование, масштабирование, поддержка', 'Sprint Book', 2024),
  -- 100017
  ('Бесцветный Цкуру Тадзаки и годы его странствий', 'Эксмо', 2023),
  -- 100018
  ('Кафка на пляже', 'Эксмо', 2017),
  -- 100019
  ('Отказ всех систем', 'Fanzon', 2020),
  -- 100020
  ('Стратегия отхода', 'Fanzon', 2020),
  -- 100021
  ('Сетевой эффект', 'Fanzon', 2020),
  -- 100022
  ('Телеметрия беглецов', 'Fanzon', 2020),
  -- 100023
  ('Жизнь насекомых', 'АСТ', 2019),
  -- 100024
  ('Жизнь насекомых', 'Азбука', 2023),
  -- 100025
  ('Мистер Мерседес', 'АСТ', 2017),
  -- 100026
  ('Детство', 'Эксмо', 2019),
  -- 100027
  ('The Bazaar of Bad Dreams: Stories', 'Scribner', 2015),
  -- 100028
  ('Soft Power: The Means To Success In World Politics', 'PublicAffairs', 2004),
  -- 100029
  ('Thinking, Fast and Slow', 'Farrar, Straus and Giroux', 2011),
  -- 100030
  ('Thinking, Fast and Slow', 'Farrar, Straus and Giroux', 2013);

-- Авторы
  CREATE TABLE IF NOT EXISTS authors(
    author_id SERIAL PRIMARY KEY,
    author VARCHAR(255) UNIQUE NOT NULL);

  DELETE FROM authors;
  ALTER SEQUENCE authors_author_id_seq RESTART WITH 1;

  INSERT INTO authors (author) values
  -- 1
  ('No authority'),
  -- 2
  ('Портянкин Иван'),
  -- 3
  ('Мэтиз Эрик'),
  -- 4
  ('Гейман Нил'),
  -- 5
  ('Пратчетт Терри'),
  -- 6
  ('Пелевин Виктор'),
  -- 7
  ('Горький Максим'),
  -- 8
  ('Савельев Владимир'),
  -- 9
  ('Зубков Сергей'),
  -- 10
  ('Клеппман Мартин'),
  -- 11
  ('Мураками Харуки'),
  -- 12
  ('Уэллс Марта'),
  -- 13
  ('Кинг Стивен'),
  -- 14
  ('King Stephen'),
  -- 15
  ('Joseph S. Nye Jr.'),
  -- 16
  ('Daniel Kahneman');

--Авторство
  CREATE TABLE IF NOT EXISTS authority(
    id SERIAL PRIMARY KEY,
    book_id INTEGER,
    author_id INTEGER DEFAULT -1,
    FOREIGN KEY (book_id) REFERENCES books (book_id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES authors (author_id) ON DELETE SET DEFAULT,
    CONSTRAINT
    unique_authority UNIQUE (book_id, author_id));

  DELETE FROM authority;
  ALTER SEQUENCE authority_id_seq RESTART WITH 1;

  INSERT INTO authority (book_id, author_id) values
  (100001, 2),
  (100002, 3),
  (100003, 4),
  (100004, 4),
  (100004, 5),
  (100005, 6),
  (100006, 6),
  (100007, 7),
  (100008, 7),
  (100009, 7),
  (100010, 1),
  (100011, 1),
  (100012, 8),
  (100013, 4),
  (100014, 4),
  (100015, 9),
  (100016, 10),
  (100017, 11),
  (100018, 11),
  (100019, 12),
  (100020, 12),
  (100021, 12),
  (100022, 12),
  (100023, 6),
  (100024, 6),
  (100025, 13),
  (100026, 7),
  (100027, 14),
  (100028, 15),
  (100029, 16),
  (100030, 16);


EOSQL

### Примеры запросов

: << 'END'

SELECT book_id, title, publisher, year, author FROM books
JOIN authority ON books.book_id = authority.book_id
JOIN authors ON authority.author_id = authors.author_id;

SELECT author FROM books
JOIN authority ON books.book_id = authority.book_id
JOIN authors ON authority.author_id = authors.author_id
WHERE books.book_id = 4;



END

