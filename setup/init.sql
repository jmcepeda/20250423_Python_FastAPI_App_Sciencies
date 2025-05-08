-- Volcado de datos para la tabla cursos
--

INSERT INTO cursos (`id`, `nombre_curso`, `level`, `created_at`) VALUES
(1, 'Guardería', 0, NULL),
(2, 'Primero de Infantil', 1, NULL),
(3, 'Segundo de Infantil', 2, NULL),
(4, 'Primero de Primaria', 3, NULL),
(5, 'Segundo de Primaria', 4, NULL),
(6, 'Tercero de Primaria', 5, NULL),
(7, 'Cuarto de Primaria', 6, NULL),
(8, 'Quinto de Primaria', 7, NULL),
(9, 'Sexto de Primaria', 8, NULL),
(10, 'Primero de Secundaria', 9, NULL),
(11, 'Segundo de Secundaria', 10, NULL),
(12, 'Tercero de Secundaria', 11, NULL),
(13, 'Cuarto de Secundaria', 12, NULL),
(14, 'Primero de Bachillerato', 13, NULL),
(15, 'Segundo de Bachillerato', 14, NULL);

--
-- Volcado de datos para la tabla asignaturas
--
-- IMPORTANTE: Los `curso_id` deben coincidir con los `id` insertados en la tabla `cursos`

INSERT INTO asignaturas (`id`, `nombre_asignatura`, `curso_id`, `created_at`) VALUES
(1, 'Sciences', 1, NULL),
(2, 'Sciences', 2, NULL),
(3, 'Sciences', 3, NULL),
(4, 'Sciences', 4, NULL),
(5, 'Sciences', 5, NULL),
(6, 'Sciences', 6, NULL),
(7, 'Sciences', 7, NULL),
(8, 'Sciences', 8, NULL),
(9, 'Sciences', 9, NULL),
(10, 'Sciences', 10, NULL),
(11, 'Sciences', 11, NULL),
(12, 'Sciences', 12, NULL),
(13, 'Sciences', 13, NULL),
(14, 'Sciences', 14, NULL),
(15, 'English', 2, NULL),
(16, 'English', 3, NULL),
(17, 'English', 4, NULL),
(18, 'English', 5, NULL),
(19, 'English', 6, NULL),
(20, 'English', 7, NULL),
(21, 'English', 8, NULL),
(22, 'English', 9, NULL),
(23, 'English', 10, NULL),
(24, 'English', 11, NULL),
(25, 'English', 12, NULL),
(26, 'English', 13, NULL);

-- Puedes añadir más inserciones aquí si tienes más datos para ambas tablas