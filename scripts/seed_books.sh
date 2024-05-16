#!/bin/bash

psql --set ON_ERROR_STOP=OFF -h localhost -U "app" -d "app"<<-EOSQL
-- Книги
  CREATE TABLE IF NOT EXISTS books(
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    publisher VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    CONSTRAINT
    unique_book UNIQUE (title, publisher, year));

  DELETE FROM books;
  ALTER SEQUENCE  books_book_id_seq  RESTART WITH 1;

  INSERT INTO books (title, publisher, year) values
  -- 1
  ('Программирование cloud native', 'Издательские решения', 2020),
  -- 2
  ('Изучаем python', 'Питер', 2022),
  -- 3
  ('Океан в конце дороги', 'АСТ', 2022),
  -- 4
  ('Благие знамения', 'Эксмо', 2023),
  -- 5
  ('Чапаев и Пустота', 'АСТ', 2023),
  -- 6
  ('Generation П', 'Азбука', '2022'),
  -- 7
  ('Детство', 'Эксмо', 2019),
  -- 8
  ('В людях', 'Эксмо', 2020),
  -- 9
  ('Мои университеты', 'Эксмо', 2021),
  -- 10
  ('Правила устройства электроустановок. Все действующие разделы ПУЭ-6 и ПУЭ-7', 'Норматика', 2020),
  -- 11
  ('СП 52.13330.2016. Свод правил. Естественное и искусственное освещение (Актуализированная редакция СНиП 23-05-95*)', 'УралЮрИздат', 2021),
  -- 12
  ('Статистика и котики', 'АСТ', 2022),
  -- 13
  ('Скандинавские боги', 'АСТ', 2019),
  -- 14
  ('Американские боги', 'АСТ', 2018),
  -- 15
  ('Для программистов. Assembler для DOS, Windows и Unix', 'ДМК Пресс', 2017),
  -- 16
  ('Высоконагруженные приложения. Программирование, масштабирование, поддержка', 'Sprint Book', 2024),
  -- 17
  ('Бесцветный Цкуру Тадзаки и годы его странствий', 'Эксмо', 2023),
  -- 18
  ('Кафка на пляже', 'Эксмо', 2017),
  -- 19
  ('Отказ всех систем', 'Fanzon', 2020),
  -- 20
  ('Стратегия отхода', 'Fanzon', 2020),
  -- 21
  ('Сетевой эффект', 'Fanzon', 2020),
  -- 22
  ('Телеметрия беглецов', 'Fanzon', 2020),
  -- 23
  ('Жизнь насекомых', 'АСТ', 2019),
  -- 24
  ('Жизнь насекомых', 'Азбука', 2023),
  -- 25
  ('Мистер Мерседес', 'АСТ', 2017);

-- Авторы
  CREATE TABLE IF NOT EXISTS authors(
    author_id SERIAL PRIMARY KEY,
    author VARCHAR(255) UNIQUE NOT NULL);

  DELETE FROM authors;
  ALTER SEQUENCE authors_author_id_seq RESTART WITH 1;

  INSERT INTO authors (author) values
  -- 1
  ('Нет авторcтва'),
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
  ('Кинг Стивен');

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
  (1, 2),
  (2, 3),
  (3, 4),
  (4, 4),
  (4, 5),
  (5, 6),
  (6, 6),
  (7, 7),
  (8, 7),
  (9, 7),
  (10, 1),
  (11, 1),
  (12, 8),
  (13, 4),
  (14, 4),
  (15, 9),
  (16, 10),
  (17, 11),
  (18, 11),
  (19, 12),
  (20, 12),
  (21, 12),
  (22, 12),
  (23, 6),
  (24, 6),
  (25, 13);


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

