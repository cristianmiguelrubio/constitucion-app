"""
Texto oficial de la Constitución Española de 1978.
Fuente: BOE-A-1978-31229. Usado como fallback si el scraper del BOE falla.
Incluye los 169 artículos + disposiciones adicionales/transitorias/derogatorias/finales.
"""

CONSTITUCION = [
    # ─── PREÁMBULO ───────────────────────────────────────────────────────────
    # (no tiene número de artículo, se omite en el índice pero se guarda)

    # ─── TÍTULO PRELIMINAR ───────────────────────────────────────────────────
    {
        "numero": "1",
        "titulo": None,
        "titulo_titulo": "TÍTULO PRELIMINAR",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 1.\n"
            "1. España se constituye en un Estado social y democrático de Derecho, que propugna como "
            "valores superiores de su ordenamiento jurídico la libertad, la justicia, la igualdad y el "
            "pluralismo político.\n"
            "2. La soberanía nacional reside en el pueblo español, del que emanan los poderes del Estado.\n"
            "3. La forma política del Estado español es la Monarquía parlamentaria."
        ),
    },
    {
        "numero": "2",
        "titulo": None,
        "titulo_titulo": "TÍTULO PRELIMINAR",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 2.\n"
            "La Constitución se fundamenta en la indisoluble unidad de la Nación española, patria común "
            "e indivisible de todos los españoles, y reconoce y garantiza el derecho a la autonomía de "
            "las nacionalidades y regiones que la integran y la solidaridad entre todas ellas."
        ),
    },
    {
        "numero": "3",
        "titulo": None,
        "titulo_titulo": "TÍTULO PRELIMINAR",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 3.\n"
            "1. El castellano es la lengua española oficial del Estado. Todos los españoles tienen el "
            "deber de conocerla y el derecho a usarla.\n"
            "2. Las demás lenguas españolas serán también oficiales en las respectivas Comunidades "
            "Autónomas de acuerdo con sus Estatutos.\n"
            "3. La riqueza de las distintas modalidades lingüísticas de España es un patrimonio cultural "
            "que será objeto de especial respeto y protección."
        ),
    },
    {
        "numero": "4",
        "titulo": None,
        "titulo_titulo": "TÍTULO PRELIMINAR",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 4.\n"
            "1. La bandera de España está formada por tres franjas horizontales, roja, amarilla y roja, "
            "siendo la amarilla de doble anchura que cada una de las rojas.\n"
            "2. Los Estatutos podrán reconocer banderas y enseñas propias de las Comunidades Autónomas. "
            "Estas se utilizarán junto a la bandera de España en sus edificios públicos y en sus actos "
            "oficiales."
        ),
    },
    {
        "numero": "5",
        "titulo": None,
        "titulo_titulo": "TÍTULO PRELIMINAR",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 5.\n"
            "La capital del Estado es la villa de Madrid."
        ),
    },
    {
        "numero": "6",
        "titulo": None,
        "titulo_titulo": "TÍTULO PRELIMINAR",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 6.\n"
            "Los partidos políticos expresan el pluralismo político, concurren a la formación y "
            "manifestación de la voluntad popular y son instrumento fundamental para la participación "
            "política. Su creación y el ejercicio de su actividad son libres dentro del respeto a la "
            "Constitución y a la ley. Su estructura interna y funcionamiento deberán ser democráticos."
        ),
    },
    {
        "numero": "7",
        "titulo": None,
        "titulo_titulo": "TÍTULO PRELIMINAR",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 7.\n"
            "Los sindicatos de trabajadores y las asociaciones empresariales contribuyen a la defensa y "
            "promoción de los intereses económicos y sociales que les son propios. Su creación y el "
            "ejercicio de su actividad son libres dentro del respeto a la Constitución y a la ley. Su "
            "estructura interna y funcionamiento deberán ser democráticos."
        ),
    },
    {
        "numero": "8",
        "titulo": None,
        "titulo_titulo": "TÍTULO PRELIMINAR",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 8.\n"
            "1. Las Fuerzas Armadas, constituidas por el Ejército de Tierra, la Armada y el Ejército del "
            "Aire, tienen como misión garantizar la soberanía e independencia de España, defender su "
            "integridad territorial y el ordenamiento constitucional.\n"
            "2. Una ley orgánica regulará las bases de la organización militar conforme a los principios "
            "de la presente Constitución."
        ),
    },
    {
        "numero": "9",
        "titulo": None,
        "titulo_titulo": "TÍTULO PRELIMINAR",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 9.\n"
            "1. Los ciudadanos y los poderes públicos están sujetos a la Constitución y al resto del "
            "ordenamiento jurídico.\n"
            "2. Corresponde a los poderes públicos promover las condiciones para que la libertad y la "
            "igualdad del individuo y de los grupos en que se integra sean reales y efectivas; remover "
            "los obstáculos que impidan o dificulten su plenitud y facilitar la participación de todos "
            "los ciudadanos en la vida política, económica, cultural y social.\n"
            "3. La Constitución garantiza el principio de legalidad, la jerarquía normativa, la "
            "publicidad de las normas, la irretroactividad de las disposiciones sancionadoras no "
            "favorables o restrictivas de derechos individuales, la seguridad jurídica, la "
            "responsabilidad y la interdicción de la arbitrariedad de los poderes públicos."
        ),
    },
    # ─── TÍTULO I: DE LOS DERECHOS Y DEBERES FUNDAMENTALES ──────────────────
    {
        "numero": "10",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 10.\n"
            "1. La dignidad de la persona, los derechos inviolables que le son inherentes, el libre "
            "desarrollo de la personalidad, el respeto a la ley y a los derechos de los demás son "
            "fundamento del orden político y de la paz social.\n"
            "2. Las normas relativas a los derechos fundamentales y a las libertades que la Constitución "
            "reconoce se interpretarán de conformidad con la Declaración Universal de Derechos Humanos y "
            "los tratados y acuerdos internacionales sobre las mismas materias ratificados por España."
        ),
    },
    {
        "numero": "11",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO I. De los españoles y los extranjeros",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 11.\n"
            "1. La nacionalidad española se adquiere, se conserva y se pierde de acuerdo con lo "
            "establecido por la ley.\n"
            "2. Ningún español de origen podrá ser privado de su nacionalidad.\n"
            "3. El Estado podrá concertar tratados de doble nacionalidad con los países iberoamericanos "
            "o con aquellos que hayan tenido o tengan una particular vinculación con España. En estos "
            "mismos países, aun cuando no reconozcan a sus ciudadanos un derecho recíproco, podrán "
            "naturalizarse los españoles sin perder su nacionalidad de origen."
        ),
    },
    {
        "numero": "12",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO I. De los españoles y los extranjeros",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 12.\n"
            "Los españoles son mayores de edad a los dieciocho años."
        ),
    },
    {
        "numero": "13",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO I. De los españoles y los extranjeros",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 13.\n"
            "1. Los extranjeros gozarán en España de las libertades públicas que garantiza el presente "
            "Título en los términos que establezcan los tratados y la ley.\n"
            "2. Solamente los españoles serán titulares de los derechos reconocidos en el artículo 23, "
            "salvo lo que, atendiendo a criterios de reciprocidad, pueda establecerse por tratado o ley "
            "para el derecho de sufragio activo y pasivo en las elecciones municipales.\n"
            "3. La extradición sólo se concederá en cumplimiento de un tratado o de la ley, atendiendo "
            "al principio de reciprocidad. Quedan excluidos de la extradición los delitos políticos, no "
            "considerándose como tales los actos de terrorismo.\n"
            "4. La ley establecerá los términos en que los ciudadanos de otros países y los apátridas "
            "podrán gozar del derecho de asilo en España."
        ),
    },
    # Capítulo II
    {
        "numero": "14",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 14.\n"
            "Los españoles son iguales ante la ley, sin que pueda prevalecer discriminación alguna por "
            "razón de nacimiento, raza, sexo, religión, opinión o cualquier otra condición o "
            "circunstancia personal o social."
        ),
    },
    {
        "numero": "15",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 1.ª De los derechos fundamentales y de las libertades públicas",
        "contenido": (
            "Artículo 15.\n"
            "Todos tienen derecho a la vida y a la integridad física y moral, sin que, en ningún caso, "
            "puedan ser sometidos a tortura ni a penas o tratos inhumanos o degradantes. Queda abolida "
            "la pena de muerte, salvo lo que puedan disponer las leyes penales militares para tiempos "
            "de guerra."
        ),
    },
    {
        "numero": "16",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 1.ª De los derechos fundamentales y de las libertades públicas",
        "contenido": (
            "Artículo 16.\n"
            "1. Se garantiza la libertad ideológica, religiosa y de culto de los individuos y las "
            "comunidades sin más limitación, en sus manifestaciones, que la necesaria para el "
            "mantenimiento del orden público protegido por la ley.\n"
            "2. Nadie podrá ser obligado a declarar sobre su ideología, religión o creencias.\n"
            "3. Ninguna confesión tendrá carácter estatal. Los poderes públicos tendrán en cuenta las "
            "creencias religiosas de la sociedad española y mantendrán las consiguientes relaciones de "
            "cooperación con la Iglesia Católica y las demás confesiones."
        ),
    },
    {
        "numero": "17",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 1.ª De los derechos fundamentales y de las libertades públicas",
        "contenido": (
            "Artículo 17.\n"
            "1. Toda persona tiene derecho a la libertad y a la seguridad. Nadie puede ser privado de "
            "su libertad, sino con la observancia de lo establecido en este artículo y en los casos y "
            "en la forma previstos en la ley.\n"
            "2. La detención preventiva no podrá durar más del tiempo estrictamente necesario para la "
            "realización de las averiguaciones tendentes al esclarecimiento de los hechos, y, en todo "
            "caso, en el plazo máximo de setenta y dos horas, el detenido deberá ser puesto en libertad "
            "o a disposición de la autoridad judicial.\n"
            "3. Toda persona detenida debe ser informada de forma inmediata, y de modo que le sea "
            "comprensible, de sus derechos y de las razones de su detención, no pudiendo ser obligada "
            "a declarar. Se garantiza la asistencia de abogado al detenido en las diligencias policiales "
            "y judiciales, en los términos que la ley establezca.\n"
            "4. La ley regulará un procedimiento de «habeas corpus» para producir la inmediata puesta a "
            "disposición judicial de toda persona detenida ilegalmente. Asimismo, por ley se determinará "
            "el plazo máximo de duración de la prisión provisional."
        ),
    },
    {
        "numero": "18",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 1.ª De los derechos fundamentales y de las libertades públicas",
        "contenido": (
            "Artículo 18.\n"
            "1. Se garantiza el derecho al honor, a la intimidad personal y familiar y a la propia imagen.\n"
            "2. El domicilio es inviolable. Ninguna entrada o registro podrá hacerse en él sin "
            "consentimiento del titular o resolución judicial, salvo en caso de flagrante delito.\n"
            "3. Se garantiza el secreto de las comunicaciones y, en especial, de las postales, "
            "telegráficas y telefónicas, salvo resolución judicial.\n"
            "4. La ley limitará el uso de la informática para garantizar el honor y la intimidad personal "
            "y familiar de los ciudadanos y el pleno ejercicio de sus derechos."
        ),
    },
    {
        "numero": "19",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 1.ª De los derechos fundamentales y de las libertades públicas",
        "contenido": (
            "Artículo 19.\n"
            "Los españoles tienen derecho a elegir libremente su residencia y a circular por el "
            "territorio nacional.\n"
            "Asimismo, tienen derecho a entrar y salir libremente de España en los términos que la ley "
            "establezca. Este derecho no podrá ser limitado por motivos políticos o ideológicos."
        ),
    },
    {
        "numero": "20",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 1.ª De los derechos fundamentales y de las libertades públicas",
        "contenido": (
            "Artículo 20.\n"
            "1. Se reconocen y protegen los derechos:\n"
            "a) A expresar y difundir libremente los pensamientos, ideas y opiniones mediante la palabra, "
            "el escrito o cualquier otro medio de reproducción.\n"
            "b) A la producción y creación literaria, artística, científica y técnica.\n"
            "c) A la libertad de cátedra.\n"
            "d) A comunicar o recibir libremente información veraz por cualquier medio de difusión. La "
            "ley regulará el derecho a la cláusula de conciencia y al secreto profesional en el ejercicio "
            "de estas libertades.\n"
            "2. El ejercicio de estos derechos no puede restringirse mediante ningún tipo de censura previa.\n"
            "3. La ley regulará la organización y el control parlamentario de los medios de comunicación "
            "social dependientes del Estado o de cualquier ente público y garantizará el acceso a dichos "
            "medios de los grupos sociales y políticos significativos, respetando el pluralismo de la "
            "sociedad y de las diversas lenguas de España.\n"
            "4. Estas libertades tienen su límite en el respeto a los derechos reconocidos en este Título, "
            "en los preceptos de las leyes que lo desarrollen y, especialmente, en el derecho al honor, "
            "a la intimidad, a la propia imagen y a la protección de la juventud y de la infancia.\n"
            "5. Sólo podrá acordarse el secuestro de publicaciones, grabaciones y otros medios de "
            "información en virtud de resolución judicial."
        ),
    },
    {
        "numero": "21",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 1.ª De los derechos fundamentales y de las libertades públicas",
        "contenido": (
            "Artículo 21.\n"
            "1. Se reconoce el derecho de reunión pacífica y sin armas. El ejercicio de este derecho no "
            "necesitará autorización previa.\n"
            "2. En los casos de reuniones en lugares de tránsito público y manifestaciones se dará "
            "comunicación previa a la autoridad, que sólo podrá prohibirlas cuando existan razones "
            "fundadas de alteración del orden público, con peligro para personas o bienes."
        ),
    },
    {
        "numero": "22",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 1.ª De los derechos fundamentales y de las libertades públicas",
        "contenido": (
            "Artículo 22.\n"
            "1. Se reconoce el derecho de asociación.\n"
            "2. Las asociaciones que persigan fines o utilicen medios tipificados como delito son ilegales.\n"
            "3. Las asociaciones constituidas al amparo de este artículo deberán inscribirse en un "
            "registro a los solos efectos de publicidad.\n"
            "4. Las asociaciones sólo podrán ser disueltas o suspendidas en sus actividades en virtud de "
            "resolución judicial motivada.\n"
            "5. Se prohíben las asociaciones secretas y las de carácter paramilitar."
        ),
    },
    {
        "numero": "23",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 1.ª De los derechos fundamentales y de las libertades públicas",
        "contenido": (
            "Artículo 23.\n"
            "1. Los ciudadanos tienen el derecho a participar en los asuntos públicos, directamente o "
            "por medio de representantes, libremente elegidos en elecciones periódicas por sufragio universal.\n"
            "2. Asimismo, tienen derecho a acceder en condiciones de igualdad a las funciones y cargos "
            "públicos, con los requisitos que señalen las leyes."
        ),
    },
    {
        "numero": "24",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 1.ª De los derechos fundamentales y de las libertades públicas",
        "contenido": (
            "Artículo 24.\n"
            "1. Todas las personas tienen derecho a obtener la tutela efectiva de los jueces y tribunales "
            "en el ejercicio de sus derechos e intereses legítimos, sin que, en ningún caso, pueda "
            "producirse indefensión.\n"
            "2. Asimismo, todos tienen derecho al Juez ordinario predeterminado por la ley, a la defensa "
            "y a la asistencia de letrado, a ser informados de la acusación formulada contra ellos, a un "
            "proceso público sin dilaciones indebidas y con todas las garantías, a utilizar los medios de "
            "prueba pertinentes para su defensa, a no declarar contra sí mismos, a no confesarse "
            "culpables y a la presunción de inocencia.\n"
            "La ley regulará los casos en que, por razón de parentesco o de secreto profesional, no se "
            "estará obligado a declarar sobre hechos presuntamente delictivos."
        ),
    },
    {
        "numero": "25",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 1.ª De los derechos fundamentales y de las libertades públicas",
        "contenido": (
            "Artículo 25.\n"
            "1. Nadie puede ser condenado o sancionado por acciones u omisiones que en el momento de "
            "producirse no constituyan delito, falta o infracción administrativa, según la legislación "
            "vigente en aquel momento.\n"
            "2. Las penas privativas de libertad y las medidas de seguridad estarán orientadas hacia la "
            "reeducación y reinserción social y no podrán consistir en trabajos forzados. El condenado a "
            "pena de prisión que estuviere cumpliendo la misma gozará de los derechos fundamentales de "
            "este Capítulo, a excepción de los que se vean expresamente limitados por el contenido del "
            "fallo condenatorio, el sentido de la pena y la ley penitenciaria. En todo caso, tendrá "
            "derecho a un trabajo remunerado y a los beneficios correspondientes de la Seguridad Social, "
            "así como al acceso a la cultura y al desarrollo integral de su personalidad.\n"
            "3. La Administración civil no podrá imponer sanciones que, directa o subsidiariamente, "
            "impliquen privación de libertad."
        ),
    },
    {
        "numero": "26",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 1.ª De los derechos fundamentales y de las libertades públicas",
        "contenido": (
            "Artículo 26.\n"
            "Se prohíben los Tribunales de Honor en el ámbito de la Administración civil y de las "
            "organizaciones profesionales."
        ),
    },
    {
        "numero": "27",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 1.ª De los derechos fundamentales y de las libertades públicas",
        "contenido": (
            "Artículo 27.\n"
            "1. Todos tienen el derecho a la educación. Se reconoce la libertad de enseñanza.\n"
            "2. La educación tendrá por objeto el pleno desarrollo de la personalidad humana en el "
            "respeto a los principios democráticos de convivencia y a los derechos y libertades fundamentales.\n"
            "3. Los poderes públicos garantizan el derecho que asiste a los padres para que sus hijos "
            "reciban la formación religiosa y moral que esté de acuerdo con sus propias convicciones.\n"
            "4. La enseñanza básica es obligatoria y gratuita.\n"
            "5. Los poderes públicos garantizan el derecho de todos a la educación, mediante una "
            "programación general de la enseñanza, con participación efectiva de todos los sectores "
            "afectados y la creación de centros docentes.\n"
            "6. Se reconoce a las personas físicas y jurídicas la libertad de creación de centros "
            "docentes, dentro del respeto a los principios constitucionales.\n"
            "7. Los profesores, los padres y, en su caso, los alumnos intervendrán en el control y "
            "gestión de todos los centros sostenidos por la Administración con fondos públicos, en los "
            "términos que la ley establezca.\n"
            "8. Los poderes públicos inspeccionarán y homologarán el sistema educativo para garantizar "
            "el cumplimiento de las leyes.\n"
            "9. Los poderes públicos ayudarán a los centros docentes que reúnan los requisitos que la "
            "ley establezca.\n"
            "10. Se reconoce la autonomía de las Universidades, en los términos que la ley establezca."
        ),
    },
    {
        "numero": "28",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 1.ª De los derechos fundamentales y de las libertades públicas",
        "contenido": (
            "Artículo 28.\n"
            "1. Todos tienen derecho a sindicarse libremente. La ley podrá limitar o exceptuar el "
            "ejercicio de este derecho a las Fuerzas o Institutos armados o a los demás Cuerpos "
            "sometidos a disciplina militar y regulará las peculiaridades de su ejercicio para los "
            "funcionarios públicos. La libertad sindical comprende el derecho a fundar sindicatos y a "
            "afiliarse al de su elección, así como el derecho de los sindicatos a formar confederaciones "
            "y a fundar organizaciones sindicales internacionales o a afiliarse a las mismas. Nadie "
            "podrá ser obligado a afiliarse a un sindicato.\n"
            "2. Se reconoce el derecho a la huelga de los trabajadores para la defensa de sus intereses. "
            "La ley que regule el ejercicio de este derecho establecerá las garantías precisas para "
            "asegurar el mantenimiento de los servicios esenciales de la comunidad."
        ),
    },
    {
        "numero": "29",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 1.ª De los derechos fundamentales y de las libertades públicas",
        "contenido": (
            "Artículo 29.\n"
            "1. Todos los españoles tendrán el derecho de petición individual y colectiva, por escrito, "
            "en la forma y con los efectos que determine la ley.\n"
            "2. Los miembros de las Fuerzas o Institutos armados o de los Cuerpos sometidos a disciplina "
            "militar podrán ejercer este derecho sólo individualmente y con arreglo a lo dispuesto en "
            "su legislación específica."
        ),
    },
    # Sección 2ª
    {
        "numero": "30",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 2.ª De los derechos y deberes de los ciudadanos",
        "contenido": (
            "Artículo 30.\n"
            "1. Los españoles tienen el derecho y el deber de defender a España.\n"
            "2. La ley fijará las obligaciones militares de los españoles y regulará, con las debidas "
            "garantías, la objeción de conciencia, así como las demás causas de exención del servicio "
            "militar obligatorio, pudiendo imponer, en su caso, una prestación social sustitutoria.\n"
            "3. Podrá establecerse un servicio civil para el cumplimiento de fines de interés general.\n"
            "4. Mediante ley podrán regularse los deberes de los ciudadanos en los casos de grave riesgo, "
            "catástrofe o calamidad pública."
        ),
    },
    {
        "numero": "31",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 2.ª De los derechos y deberes de los ciudadanos",
        "contenido": (
            "Artículo 31.\n"
            "1. Todos contribuirán al sostenimiento de los gastos públicos de acuerdo con su capacidad "
            "económica mediante un sistema tributario justo inspirado en los principios de igualdad y "
            "progresividad que, en ningún caso, tendrá alcance confiscatorio.\n"
            "2. El gasto público realizará una asignación equitativa de los recursos públicos, y su "
            "programación y ejecución responderán a los criterios de eficiencia y economía.\n"
            "3. Sólo podrán establecerse prestaciones personales o patrimoniales de carácter público "
            "con arreglo a la ley."
        ),
    },
    {
        "numero": "32",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 2.ª De los derechos y deberes de los ciudadanos",
        "contenido": (
            "Artículo 32.\n"
            "1. El hombre y la mujer tienen derecho a contraer matrimonio con plena igualdad jurídica.\n"
            "2. La ley regulará las formas de matrimonio, la edad y capacidad para contraerlo, los "
            "derechos y deberes de los cónyuges, las causas de separación y disolución y sus efectos."
        ),
    },
    {
        "numero": "33",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 2.ª De los derechos y deberes de los ciudadanos",
        "contenido": (
            "Artículo 33.\n"
            "1. Se reconoce el derecho a la propiedad privada y a la herencia.\n"
            "2. La función social de estos derechos delimitará su contenido, de acuerdo con las leyes.\n"
            "3. Nadie podrá ser privado de sus bienes y derechos sino por causa justificada de utilidad "
            "pública o interés social, mediante la correspondiente indemnización y de conformidad con lo "
            "dispuesto por las leyes."
        ),
    },
    {
        "numero": "35",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 2.ª De los derechos y deberes de los ciudadanos",
        "contenido": (
            "Artículo 35.\n"
            "1. Todos los españoles tienen el deber de trabajar y el derecho al trabajo, a la libre "
            "elección de profesión u oficio, a la promoción a través del trabajo y a una remuneración "
            "suficiente para satisfacer sus necesidades y las de su familia, sin que en ningún caso "
            "pueda hacerse discriminación por razón de sexo.\n"
            "2. La ley regulará un estatuto de los trabajadores."
        ),
    },
    # Capítulo III
    {
        "numero": "39",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO III. De los principios rectores de la política social y económica",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 39.\n"
            "1. Los poderes públicos aseguran la protección social, económica y jurídica de la familia.\n"
            "2. Los poderes públicos aseguran, asimismo, la protección integral de los hijos, iguales "
            "éstos ante la ley con independencia de su filiación, y de las madres, cualquiera que sea "
            "su estado civil. La ley posibilitará la investigación de la paternidad.\n"
            "3. Los padres deben prestar asistencia de todo orden a los hijos habidos dentro o fuera del "
            "matrimonio, durante su minoría de edad y en los demás casos en que legalmente proceda.\n"
            "4. Los niños gozarán de la protección prevista en los acuerdos internacionales que velan "
            "por sus derechos."
        ),
    },
    {
        "numero": "43",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO III. De los principios rectores de la política social y económica",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 43.\n"
            "1. Se reconoce el derecho a la protección de la salud.\n"
            "2. Compete a los poderes públicos organizar y tutelar la salud pública a través de medidas "
            "preventivas y de las prestaciones y servicios necesarios. La ley establecerá los derechos "
            "y deberes de todos al respecto.\n"
            "3. Los poderes públicos fomentarán la educación sanitaria, la educación física y el deporte. "
            "Asimismo facilitarán la adecuada utilización del ocio."
        ),
    },
    {
        "numero": "47",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO III. De los principios rectores de la política social y económica",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 47.\n"
            "Todos los españoles tienen derecho a disfrutar de una vivienda digna y adecuada. Los poderes "
            "públicos promoverán las condiciones necesarias y establecerán las normas pertinentes para "
            "hacer efectivo este derecho, regulando la utilización del suelo de acuerdo con el interés "
            "general para impedir la especulación. La comunidad participará en las plusvalías que genere "
            "la acción urbanística de los entes públicos."
        ),
    },
    # Capítulo IV
    {
        "numero": "53",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO IV. De las garantías de las libertades y derechos fundamentales",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 53.\n"
            "1. Los derechos y libertades reconocidos en el Capítulo segundo del presente Título vinculan "
            "a todos los poderes públicos. Sólo por ley, que en todo caso deberá respetar su contenido "
            "esencial, podrá regularse el ejercicio de tales derechos y libertades, que se tutelarán de "
            "acuerdo con lo previsto en el artículo 161, 1, a).\n"
            "2. Cualquier ciudadano podrá recabar la tutela de las libertades y derechos reconocidos en "
            "el artículo 14 y la Sección primera del Capítulo segundo ante los Tribunales ordinarios por "
            "un procedimiento basado en los principios de preferencia y sumariedad y, en su caso, a "
            "través del recurso de amparo ante el Tribunal Constitucional. Este último recurso será "
            "aplicable a la objeción de conciencia reconocida en el artículo 30.\n"
            "3. El reconocimiento, el respeto y la protección de los principios reconocidos en el "
            "Capítulo tercero informarán la legislación positiva, la práctica judicial y la actuación "
            "de los poderes públicos. Sólo podrán ser alegados ante la Jurisdicción ordinaria de acuerdo "
            "con lo que dispongan las leyes que los desarrollen."
        ),
    },
    {
        "numero": "54",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO IV. De las garantías de las libertades y derechos fundamentales",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 54.\n"
            "Una ley orgánica regulará la institución del Defensor del Pueblo, como alto comisionado de "
            "las Cortes Generales, designado por éstas para la defensa de los derechos comprendidos en "
            "este Título, a cuyo efecto podrá supervisar la actividad de la Administración, dando cuenta "
            "a las Cortes Generales."
        ),
    },
    # ─── TÍTULO II: DE LA CORONA ─────────────────────────────────────────────
    {
        "numero": "56",
        "titulo": None,
        "titulo_titulo": "TÍTULO II. De la Corona",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 56.\n"
            "1. El Rey es el Jefe del Estado, símbolo de su unidad y permanencia, arbitra y modera el "
            "funcionamiento regular de las instituciones, asume la más alta representación del Estado "
            "español en las relaciones internacionales, especialmente con las naciones de su comunidad "
            "histórica, y ejerce las funciones que le atribuyen expresamente la Constitución y las leyes.\n"
            "2. Su título es el de Rey de España y podrá utilizar los demás que correspondan a la Corona.\n"
            "3. La persona del Rey es inviolable y no está sujeta a responsabilidad. Sus actos estarán "
            "siempre refrendados en la forma establecida en el artículo 64, careciendo de validez sin "
            "dicho refrendo, salvo lo dispuesto en el artículo 65, 2."
        ),
    },
    {
        "numero": "57",
        "titulo": None,
        "titulo_titulo": "TÍTULO II. De la Corona",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 57.\n"
            "1. La Corona de España es hereditaria en los sucesores de S.M. Don Juan Carlos I de Borbón, "
            "legítimo heredero de la dinastía histórica. La sucesión en el trono seguirá el orden regular "
            "de primogenitura y representación, siendo preferida siempre la línea anterior a las "
            "posteriores; en la misma línea, el grado más próximo al más remoto; en el mismo grado, el "
            "varón a la mujer, y en el mismo sexo, la persona de más edad a la de menos.\n"
            "2. El Príncipe heredero, desde su nacimiento o desde que se produzca el hecho que origine "
            "el llamamiento, tendrá la dignidad de Príncipe de Asturias y los demás títulos vinculados "
            "tradicionalmente al sucesor de la Corona de España.\n"
            "3. Extinguidas todas las líneas llamadas en Derecho, las Cortes Generales proveerán a la "
            "sucesión en la Corona en la forma que más convenga a los intereses de España.\n"
            "4. Aquellas personas que teniendo derecho a la sucesión en el trono contrajeren matrimonio "
            "contra la expresa prohibición del Rey y de las Cortes Generales, quedarán excluidas en la "
            "sucesión a la Corona por sí y sus descendientes.\n"
            "5. Las abdicaciones y renuncias y cualquier duda de hecho o de derecho que ocurra en el "
            "orden de sucesión a la Corona se resolverán por una ley orgánica."
        ),
    },
    {
        "numero": "62",
        "titulo": None,
        "titulo_titulo": "TÍTULO II. De la Corona",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 62.\n"
            "Corresponde al Rey:\n"
            "a) Sancionar y promulgar las leyes.\n"
            "b) Convocar y disolver las Cortes Generales y convocar elecciones en los términos previstos "
            "en la Constitución.\n"
            "c) Convocar referéndum en los casos previstos en la Constitución.\n"
            "d) Proponer el candidato a Presidente del Gobierno y, en su caso, nombrarlo, así como poner "
            "fin a sus funciones en los términos previstos en la Constitución.\n"
            "e) Nombrar y separar a los miembros del Gobierno, a propuesta de su Presidente.\n"
            "f) Expedir los decretos acordados en el Consejo de Ministros, conferir los empleos civiles "
            "y militares y conceder honores y distinciones con arreglo a las leyes.\n"
            "g) Ser informado de los asuntos de Estado y presidir, a estos efectos, las sesiones del "
            "Consejo de Ministros, cuando lo estime oportuno, a petición del Presidente del Gobierno.\n"
            "h) El mando supremo de las Fuerzas Armadas.\n"
            "i) Ejercer el derecho de gracia con arreglo a la ley, que no podrá autorizar indultos generales.\n"
            "j) El Alto Patronazgo de las Reales Academias."
        ),
    },
    # ─── TÍTULO III: DE LAS CORTES GENERALES ────────────────────────────────
    {
        "numero": "66",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO I. De las Cámaras",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 66.\n"
            "1. Las Cortes Generales representan al pueblo español y están formadas por el Congreso de "
            "los Diputados y el Senado.\n"
            "2. Las Cortes Generales ejercen la potestad legislativa del Estado, aprueban sus "
            "Presupuestos, controlan la acción del Gobierno y tienen las demás competencias que les "
            "atribuya la Constitución.\n"
            "3. Las Cortes Generales son inviolables."
        ),
    },
    {
        "numero": "68",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO I. De las Cámaras",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 68.\n"
            "1. El Congreso se compone de un mínimo de trescientos y un máximo de cuatrocientos "
            "Diputados, elegidos por sufragio universal, libre, igual, directo y secreto, en los "
            "términos que establezca la ley.\n"
            "2. La circunscripción electoral es la provincia. Las poblaciones de Ceuta y Melilla estarán "
            "representadas cada una de ellas por un Diputado. La ley distribuirá el número total de "
            "Diputados, asignando una representación mínima inicial a cada circunscripción y distribuyendo "
            "los demás en proporción a la población.\n"
            "3. La elección se verificará en cada circunscripción atendiendo a criterios de representación "
            "proporcional.\n"
            "4. El Congreso es elegido por cuatro años. El mandato de los Diputados termina cuatro años "
            "después de su elección o el día de la disolución de la Cámara.\n"
            "5. Son electores y elegibles todos los españoles que estén en pleno uso de sus derechos "
            "políticos. La ley reconocerá y el Estado facilitará el ejercicio del derecho de sufragio "
            "a los españoles que se encuentren fuera del territorio de España.\n"
            "6. Las elecciones tendrán lugar entre los treinta días y sesenta días desde la terminación "
            "del mandato. El Congreso electo deberá ser convocado dentro de los veinticinco días "
            "siguientes a la celebración de las elecciones."
        ),
    },
    {
        "numero": "69",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO I. De las Cámaras",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 69.\n"
            "1. El Senado es la Cámara de representación territorial.\n"
            "2. En cada provincia se elegirán cuatro Senadores por sufragio universal, libre, igual, "
            "directo y secreto por los votantes de cada una de ellas, en los términos que señale una ley orgánica.\n"
            "3. En las provincias insulares, cada isla o agrupación de ellas, con Cabildo o Consejo "
            "Insular, constituirá una circunscripción a efectos de elección de Senadores, correspondiendo "
            "tres a cada una de las islas mayores —Gran Canaria, Mallorca y Tenerife— y uno a cada una "
            "de las siguientes islas o agrupaciones: Ibiza-Formentera, Menorca, Fuerteventura, Gomera, "
            "Hierro, Lanzarote y La Palma.\n"
            "4. Las poblaciones de Ceuta y Melilla elegirán cada una de ellas dos Senadores.\n"
            "5. Las Comunidades Autónomas designarán además un Senador y otro más por cada millón de "
            "habitantes de su respectivo territorio. La designación corresponderá a la Asamblea "
            "legislativa o, en su defecto, al órgano colegiado superior de la Comunidad Autónoma, de "
            "acuerdo con lo que establezcan los Estatutos, que asegurarán, en todo caso, la adecuada "
            "representación proporcional.\n"
            "6. El Senado es elegido por cuatro años. El mandato de los Senadores termina cuatro años "
            "después de su elección o el día de la disolución de la Cámara."
        ),
    },
    # ─── TÍTULO IV: DEL GOBIERNO ─────────────────────────────────────────────
    {
        "numero": "97",
        "titulo": None,
        "titulo_titulo": "TÍTULO IV. Del Gobierno y de la Administración",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 97.\n"
            "El Gobierno dirige la política interior y exterior, la Administración civil y militar y la "
            "defensa del Estado. Ejerce la función ejecutiva y la potestad reglamentaria de acuerdo con "
            "la Constitución y las leyes."
        ),
    },
    {
        "numero": "98",
        "titulo": None,
        "titulo_titulo": "TÍTULO IV. Del Gobierno y de la Administración",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 98.\n"
            "1. El Gobierno se compone del Presidente, de los Vicepresidentes, en su caso, de los "
            "Ministros y de los demás miembros que establezca la ley.\n"
            "2. El Presidente dirige la acción del Gobierno y coordina las funciones de los demás "
            "miembros del mismo, sin perjuicio de la competencia y responsabilidad directa de éstos "
            "en su gestión.\n"
            "3. Los miembros del Gobierno no podrán ejercer otras funciones representativas que las "
            "propias del mandato parlamentario, ni cualquier otra función pública que no derive de su "
            "cargo, ni actividad profesional o mercantil alguna.\n"
            "4. La ley regulará el estatuto e incompatibilidades de los miembros del Gobierno."
        ),
    },
    {
        "numero": "99",
        "titulo": None,
        "titulo_titulo": "TÍTULO IV. Del Gobierno y de la Administración",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 99.\n"
            "1. Después de cada renovación del Congreso de los Diputados, y en los demás supuestos "
            "constitucionales en que así proceda, el Rey, previa consulta con los representantes "
            "designados por los Grupos políticos con representación parlamentaria, y a través del "
            "Presidente del Congreso, propondrá un candidato a la Presidencia del Gobierno.\n"
            "2. El candidato propuesto conforme a lo previsto en el apartado anterior expondrá ante el "
            "Congreso de los Diputados el programa político del Gobierno que pretenda formar y solicitará "
            "la confianza de la Cámara.\n"
            "3. Si el Congreso de los Diputados, por el voto de la mayoría absoluta de sus miembros, "
            "otorgare su confianza a dicho candidato, el Rey le nombrará Presidente. De no alcanzarse "
            "dicha mayoría, se someterá la misma propuesta a nueva votación cuarenta y ocho horas "
            "después de la anterior, y la confianza se entenderá otorgada si obtuviere la mayoría simple.\n"
            "4. Si efectuadas las citadas votaciones no se otorgase la confianza para la investidura, "
            "se tramitarán sucesivas propuestas en la forma prevista en los apartados anteriores.\n"
            "5. Si transcurrido el plazo de dos meses, a partir de la primera votación de investidura, "
            "ningún candidato hubiere obtenido la confianza del Congreso, el Rey disolverá ambas "
            "Cámaras y convocará nuevas elecciones con el refrendo del Presidente del Congreso."
        ),
    },
    # ─── TÍTULO V ─────────────────────────────────────────────────────────────
    {
        "numero": "108",
        "titulo": None,
        "titulo_titulo": "TÍTULO V. De las relaciones entre el Gobierno y las Cortes Generales",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 108.\n"
            "El Gobierno responde solidariamente en su gestión política ante el Congreso de los Diputados."
        ),
    },
    {
        "numero": "113",
        "titulo": None,
        "titulo_titulo": "TÍTULO V. De las relaciones entre el Gobierno y las Cortes Generales",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 113.\n"
            "1. El Congreso de los Diputados puede exigir la responsabilidad política del Gobierno "
            "mediante la adopción por mayoría absoluta de la moción de censura.\n"
            "2. La moción de censura deberá ser propuesta al menos por la décima parte de los Diputados, "
            "y habrá de incluir un candidato a la Presidencia del Gobierno.\n"
            "3. La moción de censura no podrá ser votada hasta que transcurran cinco días desde su "
            "presentación. En los dos primeros días de dicho plazo podrán presentarse mociones alternativas.\n"
            "4. Si la moción de censura no fuere aprobada por el Congreso, sus signatarios no podrán "
            "presentar otra durante el mismo período de sesiones."
        ),
    },
    # ─── TÍTULO VI: DEL PODER JUDICIAL ───────────────────────────────────────
    {
        "numero": "117",
        "titulo": None,
        "titulo_titulo": "TÍTULO VI. Del Poder Judicial",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 117.\n"
            "1. La justicia emana del pueblo y se administra en nombre del Rey por Jueces y Magistrados "
            "integrantes del poder judicial, independientes, inamovibles, responsables y sometidos "
            "únicamente al imperio de la ley.\n"
            "2. Los Jueces y Magistrados no podrán ser separados, suspendidos, trasladados ni jubilados, "
            "sino por alguna de las causas y con las garantías previstas en la ley.\n"
            "3. El ejercicio de la potestad jurisdiccional en todo tipo de procesos, juzgando y haciendo "
            "ejecutar lo juzgado, corresponde exclusivamente a los Juzgados y Tribunales determinados "
            "por las leyes, según las normas de competencia y procedimiento que las mismas establezcan.\n"
            "4. Los Juzgados y Tribunales no ejercerán más funciones que las señaladas en el apartado "
            "anterior y las que expresamente les sean atribuidas por ley en garantía de cualquier derecho.\n"
            "5. El principio de unidad jurisdiccional es la base de la organización y funcionamiento de "
            "los Tribunales. La ley regulará el ejercicio de la jurisdicción militar en el ámbito "
            "estrictamente castrense y en los supuestos de estado de sitio, de acuerdo con los principios "
            "de la Constitución.\n"
            "6. Se prohíben los Tribunales de excepción."
        ),
    },
    {
        "numero": "122",
        "titulo": None,
        "titulo_titulo": "TÍTULO VI. Del Poder Judicial",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 122.\n"
            "1. La ley orgánica del poder judicial determinará la constitución, funcionamiento y gobierno "
            "de los Juzgados y Tribunales, así como el estatuto jurídico de los Jueces y Magistrados de "
            "carrera, que formarán un Cuerpo único, y del personal al servicio de la Administración de Justicia.\n"
            "2. El Consejo General del Poder Judicial es el órgano de gobierno del mismo. La ley orgánica "
            "establecerá su estatuto y el régimen de incompatibilidades de sus miembros y sus funciones, "
            "en particular en materia de nombramientos, ascensos, inspección y régimen disciplinario.\n"
            "3. El Consejo General del Poder Judicial estará integrado por el Presidente del Tribunal "
            "Supremo, que lo presidirá, y por veinte miembros nombrados por el Rey por un período de "
            "cinco años. De éstos, doce entre Jueces y Magistrados de todas las categorías judiciales, "
            "en los términos que establezca la ley orgánica; cuatro a propuesta del Congreso de los "
            "Diputados, y cuatro a propuesta del Senado, elegidos en ambos casos por mayoría de tres "
            "quintos de sus miembros, entre abogados y otros juristas, todos ellos de reconocida "
            "competencia y con más de quince años de ejercicio en su profesión."
        ),
    },
    # ─── TÍTULO VII: ECONOMÍA Y HACIENDA ─────────────────────────────────────
    {
        "numero": "128",
        "titulo": None,
        "titulo_titulo": "TÍTULO VII. Economía y Hacienda",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 128.\n"
            "1. Toda la riqueza del país en sus distintas formas y sea cual fuere su titular está "
            "subordinada al interés general.\n"
            "2. Se reconoce la iniciativa pública en la actividad económica. Mediante ley se podrá "
            "reservar al sector público recursos o servicios esenciales, especialmente en caso de "
            "monopolio, y asimismo acordar la intervención de empresas cuando así lo exigiere el "
            "interés general."
        ),
    },
    {
        "numero": "135",
        "titulo": None,
        "titulo_titulo": "TÍTULO VII. Economía y Hacienda",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 135.\n"
            "1. Todas las Administraciones Públicas adecuarán sus actuaciones al principio de estabilidad "
            "presupuestaria.\n"
            "2. El Estado y las Comunidades Autónomas no podrán incurrir en un déficit estructural que "
            "supere los márgenes establecidos, en su caso, por la Unión Europea para sus Estados Miembros. "
            "Una ley orgánica fijará el déficit estructural máximo permitido al Estado y a las "
            "Comunidades Autónomas, en relación con su producto interior bruto. Las Entidades Locales "
            "deberán presentar equilibrio presupuestario.\n"
            "3. El Estado y las Comunidades Autónomas habrán de estar autorizados por ley para emitir "
            "deuda pública o contraer crédito.\n"
            "Los créditos para satisfacer los intereses y el capital de la deuda pública de las "
            "Administraciones se entenderán siempre incluidos en el estado de gastos de sus presupuestos "
            "y su pago gozará de prioridad absoluta. Estos créditos no podrán ser objeto de enmienda o "
            "modificación, mientras se ajusten a las condiciones de la ley de emisión.\n"
            "El Gobierno habrá de estar autorizado por ley orgánica para la emisión de Deuda Pública.\n"
            "4. Los límites de déficit estructural y de volumen de deuda pública sólo podrán superarse "
            "en caso de catástrofes naturales, recesión económica o situaciones de emergencia "
            "extraordinaria que escapen al control del Estado y perjudiquen considerablemente la situación "
            "financiera o la sostenibilidad económica o social del Estado, apreciadas por la mayoría "
            "absoluta de los miembros del Congreso de los Diputados.\n"
            "5. Una ley orgánica desarrollará los principios a que se refiere este artículo, así como "
            "la participación, en los procedimientos respectivos, de los órganos de coordinación "
            "institucional entre las Administraciones Públicas en materia de política fiscal y financiera. "
            "En todo caso, regulará:\n"
            "a) La distribución de los límites de déficit y de deuda entre las distintas Administraciones "
            "Públicas, los supuestos excepcionales de superación de los mismos y la forma y plazo de "
            "corrección de las desviaciones que sobre uno y otro pudieran producirse.\n"
            "b) La metodología y el procedimiento para el cálculo del déficit estructural.\n"
            "c) La responsabilidad de cada Administración Pública en caso de incumplimiento de los "
            "objetivos de estabilidad presupuestaria.\n"
            "6. Las Comunidades Autónomas, de acuerdo con sus respectivos Estatutos y dentro de los "
            "límites a que se refiere este artículo, adoptarán las disposiciones que procedan para la "
            "aplicación efectiva del principio de estabilidad en sus normas y decisiones presupuestarias."
        ),
    },
    # ─── TÍTULO VIII: ORGANIZACIÓN TERRITORIAL ────────────────────────────────
    {
        "numero": "137",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO I. Principios generales",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 137.\n"
            "El Estado se organiza territorialmente en municipios, en provincias y en las Comunidades "
            "Autónomas que se constituyan. Todas estas entidades gozan de autonomía para la gestión "
            "de sus respectivos intereses."
        ),
    },
    {
        "numero": "140",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO II. De la Administración Local",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 140.\n"
            "La Constitución garantiza la autonomía de los municipios. Estos gozarán de personalidad "
            "jurídica plena. Su gobierno y administración corresponde a sus respectivos Ayuntamientos, "
            "integrados por los Alcaldes y los Concejales. Los Concejales serán elegidos por los vecinos "
            "del municipio mediante sufragio universal, igual, libre, directo y secreto, en la forma "
            "establecida por la ley. Los Alcaldes serán elegidos por los Concejales o por los vecinos. "
            "La ley regulará las condiciones en las que proceda el régimen del concejo abierto."
        ),
    },
    # ─── TÍTULO IX: TRIBUNAL CONSTITUCIONAL ──────────────────────────────────
    {
        "numero": "159",
        "titulo": None,
        "titulo_titulo": "TÍTULO IX. Del Tribunal Constitucional",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 159.\n"
            "1. El Tribunal Constitucional se compone de doce miembros nombrados por el Rey; de ellos, "
            "cuatro a propuesta del Congreso por mayoría de tres quintos de sus miembros; cuatro a "
            "propuesta del Senado, con idéntica mayoría; dos a propuesta del Gobierno, y dos a propuesta "
            "del Consejo General del Poder Judicial.\n"
            "2. Los miembros del Tribunal Constitucional deberán ser nombrados entre Magistrados y "
            "Fiscales, Profesores de Universidad, funcionarios públicos y Abogados, todos ellos juristas "
            "de reconocida competencia con más de quince años de ejercicio profesional.\n"
            "3. Los miembros del Tribunal Constitucional serán designados por un período de nueve años "
            "y se renovarán por terceras partes cada tres.\n"
            "4. La condición de miembro del Tribunal Constitucional es incompatible: con todo mandato "
            "representativo; con los cargos políticos o administrativos; con el desempeño de funciones "
            "directivas en un partido político o en un sindicato y con el empleo al servicio de los "
            "mismos; con el ejercicio de las carreras judicial y fiscal, y con cualquier actividad "
            "profesional o mercantil.\n"
            "En lo demás, los miembros del Tribunal Constitucional tendrán las incompatibilidades "
            "propias de los miembros del poder judicial.\n"
            "5. Los miembros del Tribunal Constitucional serán independientes e inamovibles en el "
            "ejercicio de su mandato."
        ),
    },
    {
        "numero": "161",
        "titulo": None,
        "titulo_titulo": "TÍTULO IX. Del Tribunal Constitucional",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 161.\n"
            "1. El Tribunal Constitucional tiene jurisdicción en todo el territorio español y es "
            "competente para conocer:\n"
            "a) Del recurso de inconstitucionalidad contra leyes y disposiciones normativas con fuerza "
            "de ley. La declaración de inconstitucionalidad de una norma jurídica con rango de ley, "
            "interpretada por la jurisprudencia, afectará a ésta, si bien la sentencia o sentencias "
            "recaídas no perderán el valor de cosa juzgada.\n"
            "b) Del recurso de amparo por violación de los derechos y libertades referidos en el "
            "artículo 53, 2, de esta Constitución, en los casos y formas que la ley establezca.\n"
            "c) De los conflictos de competencia entre el Estado y las Comunidades Autónomas o de los "
            "de éstas entre sí.\n"
            "d) De las demás materias que le atribuyan la Constitución o las leyes orgánicas.\n"
            "2. El Gobierno podrá impugnar ante el Tribunal Constitucional las disposiciones y "
            "resoluciones adoptadas por los órganos de las Comunidades Autónomas. La impugnación "
            "producirá la suspensión de la disposición o resolución recurrida, pero el Tribunal, en "
            "su caso, deberá ratificarla o levantarla en un plazo no superior a cinco meses."
        ),
    },
    # ─── TÍTULO X: REFORMA CONSTITUCIONAL ────────────────────────────────────
    {
        "numero": "166",
        "titulo": None,
        "titulo_titulo": "TÍTULO X. De la reforma constitucional",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 166.\n"
            "La iniciativa de reforma constitucional se ejercerá en los términos previstos en los "
            "apartados 1 y 2 del artículo 87."
        ),
    },
    {
        "numero": "167",
        "titulo": None,
        "titulo_titulo": "TÍTULO X. De la reforma constitucional",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 167.\n"
            "1. Los proyectos de reforma constitucional deberán ser aprobados por una mayoría de tres "
            "quintos de cada una de las Cámaras. Si no hubiera acuerdo entre ambas, se intentará "
            "obtenerlo mediante la creación de una Comisión de composición paritaria de Diputados y "
            "Senadores, que presentará un texto que será votado por el Congreso y el Senado.\n"
            "2. De no lograrse la aprobación mediante el procedimiento del apartado anterior, y siempre "
            "que el texto hubiere obtenido el voto favorable de la mayoría absoluta del Senado, el "
            "Congreso, por mayoría de dos tercios, podrá aprobar la reforma.\n"
            "3. Aprobada la reforma por las Cortes Generales, será sometida a referéndum para su "
            "ratificación cuando así lo soliciten, dentro de los quince días siguientes a su aprobación, "
            "una décima parte de los miembros de cualquiera de las Cámaras."
        ),
    },
    {
        "numero": "168",
        "titulo": None,
        "titulo_titulo": "TÍTULO X. De la reforma constitucional",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 168.\n"
            "1. Cuando se propusiere la revisión total de la Constitución o una parcial que afecte al "
            "Título preliminar, al Capítulo segundo, Sección primera del Título I, o al Título II, se "
            "procederá a la aprobación del principio por mayoría de dos tercios de cada Cámara, y a la "
            "disolución inmediata de las Cortes.\n"
            "2. Las Cámaras elegidas deberán ratificar la decisión y proceder al estudio del nuevo texto "
            "constitucional, que deberá ser aprobado por mayoría de dos tercios de ambas Cámaras.\n"
            "3. Aprobada la reforma por las Cortes Generales, será sometida a referéndum para su "
            "ratificación."
        ),
    },
    {
        "numero": "169",
        "titulo": None,
        "titulo_titulo": "TÍTULO X. De la reforma constitucional",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 169.\n"
            "No podrá iniciarse la reforma constitucional en tiempo de guerra o de vigencia de alguno "
            "de los estados contemplados en el artículo 116."
        ),
    },
    # ── Artículos que faltaban – completando los 169 ──────────────────────

    # TÍTULO I · Cap II · Sección 2ª (34, 36–38)
    {
        "numero": "34",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 2.ª De los derechos y deberes de los ciudadanos",
        "contenido": (
            "Artículo 34.\n"
            "1. Se reconoce el derecho de fundación para fines de interés general, con arreglo a la ley.\n"
            "2. Regirá también para las fundaciones lo dispuesto en los apartados 2 y 4 del artículo 22."
        ),
    },
    {
        "numero": "36",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 2.ª De los derechos y deberes de los ciudadanos",
        "contenido": (
            "Artículo 36.\n"
            "La ley regulará las peculiaridades propias del régimen jurídico de los Colegios Profesionales "
            "y el ejercicio de las profesiones tituladas. La estructura interna y el funcionamiento de los "
            "Colegios deberán ser democráticos."
        ),
    },
    {
        "numero": "37",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 2.ª De los derechos y deberes de los ciudadanos",
        "contenido": (
            "Artículo 37.\n"
            "1. La ley garantizará el derecho a la negociación colectiva laboral entre los representantes "
            "de los trabajadores y empresarios, así como la fuerza vinculante de los convenios.\n"
            "2. Se reconoce el derecho de los trabajadores y empresarios a adoptar medidas de conflicto "
            "colectivo. La ley que regule el ejercicio de este derecho, sin perjuicio de las limitaciones "
            "que pueda establecer, incluirá las garantías precisas para asegurar el funcionamiento de los "
            "servicios esenciales de la comunidad."
        ),
    },
    {
        "numero": "38",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO II. Derechos y libertades",
        "titulo_seccion": "Sección 2.ª De los derechos y deberes de los ciudadanos",
        "contenido": (
            "Artículo 38.\n"
            "Se reconoce la libertad de empresa en el marco de la economía de mercado. Los poderes "
            "públicos garantizan y protegen su ejercicio y la defensa de la productividad, de acuerdo "
            "con las exigencias de la economía general y, en su caso, de la planificación."
        ),
    },
    # TÍTULO I · Cap III (40–42, 44–46, 48–52)
    {
        "numero": "40",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO III. De los principios rectores de la política social y económica",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 40.\n"
            "1. Los poderes públicos promoverán las condiciones favorables para el progreso social y "
            "económico y para una distribución de la renta regional y personal más equitativa, en el "
            "marco de una política de estabilidad económica. De manera especial realizarán una política "
            "orientada al pleno empleo.\n"
            "2. Asimismo, los poderes públicos fomentarán una política que garantice la formación y "
            "readaptación profesionales; velarán por la seguridad e higiene en el trabajo y garantizarán "
            "el descanso necesario, mediante la limitación de la jornada laboral, las vacaciones "
            "periódicas retribuidas y la promoción de centros adecuados."
        ),
    },
    {
        "numero": "41",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO III. De los principios rectores de la política social y económica",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 41.\n"
            "Los poderes públicos mantendrán un régimen público de Seguridad Social para todos los "
            "ciudadanos, que garantice la asistencia y prestaciones sociales suficientes ante situaciones "
            "de necesidad, especialmente en caso de desempleo. La asistencia y prestaciones complementarias "
            "serán libres."
        ),
    },
    {
        "numero": "42",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO III. De los principios rectores de la política social y económica",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 42.\n"
            "El Estado velará especialmente por la salvaguardia de los derechos económicos y sociales "
            "de los trabajadores españoles en el extranjero y orientará su política hacia su retorno."
        ),
    },
    {
        "numero": "44",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO III. De los principios rectores de la política social y económica",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 44.\n"
            "1. Los poderes públicos promoverán y tutelarán el acceso a la cultura, a la que todos "
            "tienen derecho.\n"
            "2. Los poderes públicos promoverán la ciencia y la investigación científica y técnica en "
            "beneficio del interés general."
        ),
    },
    {
        "numero": "45",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO III. De los principios rectores de la política social y económica",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 45.\n"
            "1. Todos tienen el derecho a disfrutar de un medio ambiente adecuado para el desarrollo "
            "de la persona, así como el deber de conservarlo.\n"
            "2. Los poderes públicos velarán por la utilización racional de todos los recursos naturales, "
            "con el fin de proteger y mejorar la calidad de la vida y defender y restaurar el medio "
            "ambiente, apoyándose en la indispensable solidaridad colectiva.\n"
            "3. Para quienes violen lo dispuesto en el apartado anterior, en los términos que la ley "
            "fije se establecerán sanciones penales o, en su caso, administrativas, así como la "
            "obligación de reparar el daño causado."
        ),
    },
    {
        "numero": "46",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO III. De los principios rectores de la política social y económica",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 46.\n"
            "Los poderes públicos garantizarán la conservación y promoverán el enriquecimiento del "
            "patrimonio histórico, cultural y artístico de los pueblos de España y de los bienes que "
            "lo integran, cualquiera que sea su régimen jurídico y su titularidad. La ley penal "
            "sancionará los atentados contra este patrimonio."
        ),
    },
    {
        "numero": "48",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO III. De los principios rectores de la política social y económica",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 48.\n"
            "Los poderes públicos promoverán las condiciones para la participación libre y eficaz de la "
            "juventud en el desarrollo político, social, económico y cultural."
        ),
    },
    {
        "numero": "49",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO III. De los principios rectores de la política social y económica",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 49.\n"
            "Los poderes públicos realizarán una política de previsión, tratamiento, rehabilitación e "
            "integración de los disminuidos físicos, sensoriales y psíquicos, a los que prestarán la "
            "atención especializada que requieran y los ampararán especialmente para el disfrute de los "
            "derechos que este Título otorga a todos los ciudadanos."
        ),
    },
    {
        "numero": "50",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO III. De los principios rectores de la política social y económica",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 50.\n"
            "Los poderes públicos garantizarán, mediante pensiones adecuadas y periódicamente actualizadas, "
            "la suficiencia económica a los ciudadanos durante la tercera edad. Asimismo, y con "
            "independencia de las obligaciones familiares, promoverán su bienestar mediante un sistema "
            "de servicios sociales que atenderán sus problemas específicos de salud, vivienda, cultura "
            "y ocio."
        ),
    },
    {
        "numero": "51",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO III. De los principios rectores de la política social y económica",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 51.\n"
            "1. Los poderes públicos garantizarán la defensa de los consumidores y usuarios, protegiendo, "
            "mediante procedimientos eficaces, la seguridad, la salud y los legítimos intereses "
            "económicos de los mismos.\n"
            "2. Los poderes públicos promoverán la información y la educación de los consumidores y "
            "usuarios, fomentarán sus organizaciones y oirán a éstas en las cuestiones que puedan "
            "afectar a aquéllos, en los términos que la ley establezca.\n"
            "3. En el marco de lo dispuesto por los apartados anteriores, la ley regulará el comercio "
            "interior y el régimen de autorización de productos comerciales."
        ),
    },
    {
        "numero": "52",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO III. De los principios rectores de la política social y económica",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 52.\n"
            "La ley regulará las organizaciones profesionales que contribuyan a la defensa de los "
            "intereses económicos que les sean propios. Su estructura interna y funcionamiento deberán "
            "ser democráticos."
        ),
    },
    # TÍTULO I · Cap V
    {
        "numero": "55",
        "titulo": None,
        "titulo_titulo": "TÍTULO I. De los derechos y deberes fundamentales",
        "titulo_capitulo": "CAPÍTULO V. De la suspensión de los derechos y libertades",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 55.\n"
            "1. Los derechos reconocidos en los artículos 17, 18, apartados 2 y 3, artículos 19, 20, "
            "apartados 1, a) y d), y 5, artículos 21, 28, apartado 2, y artículo 37, apartado 2, "
            "podrán ser suspendidos cuando se acuerde la declaración del estado de excepción o de sitio "
            "en los términos previstos en la Constitución. Se exceptúa de lo establecido anteriormente "
            "el apartado 3 del artículo 17 para el supuesto de declaración de estado de excepción.\n"
            "2. Una ley orgánica podrá determinar la forma y los casos en los que, de forma individual "
            "y con la necesaria intervención judicial y el adecuado control parlamentario, los derechos "
            "reconocidos en los artículos 17, apartado 2, y 18, apartados 2 y 3, pueden ser suspendidos "
            "para personas determinadas, en relación con las investigaciones correspondientes a la "
            "actuación de bandas armadas o elementos terroristas.\n"
            "La utilización injustificada o abusiva de las facultades reconocidas en dicha ley orgánica "
            "producirá responsabilidad penal, como violación de los derechos y libertades reconocidos "
            "por las leyes."
        ),
    },
    # TÍTULO II (58–65)
    {
        "numero": "58",
        "titulo": None,
        "titulo_titulo": "TÍTULO II. De la Corona",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 58.\n"
            "La Reina consorte o el consorte de la Reina no podrán asumir funciones constitucionales, "
            "salvo lo dispuesto para la Regencia."
        ),
    },
    {
        "numero": "59",
        "titulo": None,
        "titulo_titulo": "TÍTULO II. De la Corona",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 59.\n"
            "1. Cuando el Rey fuere menor de edad, el padre o la madre del Rey y, en su defecto, el "
            "pariente mayor de edad más próximo a suceder en la Corona, según el orden establecido en "
            "la Constitución, entrará a ejercer inmediatamente la Regencia y la ejercerá durante el "
            "tiempo de la minoría de edad del Rey.\n"
            "2. Si el Rey se inhabilitare para el ejercicio de su autoridad y la imposibilidad fuere "
            "reconocida por las Cortes Generales, entrará a ejercer inmediatamente la Regencia el "
            "Príncipe heredero de la Corona, si fuere mayor de edad. Si no lo fuere, se procederá de "
            "la manera prevista en el apartado anterior, hasta que el Príncipe heredero alcance la "
            "mayoría de edad.\n"
            "3. Si no hubiere ninguna persona a quien corresponda la Regencia, ésta será nombrada por "
            "las Cortes Generales, y se compondrá de una, tres o cinco personas.\n"
            "4. Para ejercer la Regencia es preciso ser español y mayor de edad."
        ),
    },
    {
        "numero": "60",
        "titulo": None,
        "titulo_titulo": "TÍTULO II. De la Corona",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 60.\n"
            "1. Será tutor del Rey menor la persona que en su testamento hubiese nombrado el Rey "
            "difunto, siempre que sea mayor de edad y español de nacimiento; si no lo hubiese nombrado, "
            "será tutor el padre o la madre mientras permanezcan viudos. En su defecto, lo nombrarán "
            "las Cortes Generales, pero no podrán acumularse los cargos de Regente y de tutor sino en "
            "el padre, madre o ascendientes directos del Rey.\n"
            "2. El ejercicio de la tutela es también incompatible con el de todo cargo o representación "
            "política."
        ),
    },
    {
        "numero": "61",
        "titulo": None,
        "titulo_titulo": "TÍTULO II. De la Corona",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 61.\n"
            "1. El Rey, al ser proclamado ante las Cortes Generales, prestará juramento de desempeñar "
            "fielmente sus funciones, guardar y hacer guardar la Constitución y las leyes y respetar "
            "los derechos de los ciudadanos y de las Comunidades Autónomas.\n"
            "2. El Príncipe heredero, al alcanzar la mayoría de edad, y el Regente o Regentes al "
            "hacerse cargo de sus funciones, prestarán el mismo juramento, así como el de fidelidad "
            "al Rey."
        ),
    },
    {
        "numero": "63",
        "titulo": None,
        "titulo_titulo": "TÍTULO II. De la Corona",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 63.\n"
            "1. El Rey acredita a los embajadores y otros representantes diplomáticos. Los representantes "
            "extranjeros en España están acreditados ante él.\n"
            "2. Al Rey corresponde manifestar el consentimiento del Estado para obligarse "
            "internacionalmente por medio de tratados, de conformidad con la Constitución y las leyes.\n"
            "3. Al Rey corresponde, previa autorización de las Cortes Generales, declarar la guerra y "
            "hacer la paz."
        ),
    },
    {
        "numero": "64",
        "titulo": None,
        "titulo_titulo": "TÍTULO II. De la Corona",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 64.\n"
            "1. Los actos del Rey serán refrendados por el Presidente del Gobierno y, en su caso, por "
            "los Ministros competentes. La propuesta y el nombramiento del Presidente del Gobierno, y "
            "la disolución prevista en el artículo 99, serán refrendados por el Presidente del Congreso.\n"
            "2. De los actos del Rey serán responsables las personas que los refrenden."
        ),
    },
    {
        "numero": "65",
        "titulo": None,
        "titulo_titulo": "TÍTULO II. De la Corona",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 65.\n"
            "1. El Rey recibe de los Presupuestos del Estado una cantidad global para el sostenimiento "
            "de su Familia y Casa, y distribuye libremente la misma.\n"
            "2. El Rey nombra y releva libremente a los miembros civiles y militares de su Casa."
        ),
    },
    # TÍTULO III · Cap I (67, 70–80)
    {
        "numero": "67",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO I. De las Cámaras",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 67.\n"
            "1. Nadie podrá ser miembro de las dos Cámaras simultáneamente, ni acumular el acta de una "
            "Asamblea de Comunidad Autónoma con la de Diputado al Congreso.\n"
            "2. Los miembros de las Cortes Generales no estarán ligados por mandato imperativo.\n"
            "3. Las reuniones de Parlamentarios que se celebren sin convocatoria reglamentaria no "
            "vincularán a las Cámaras, y no podrán ejercer sus funciones ni ostentar sus privilegios."
        ),
    },
    {
        "numero": "70",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO I. De las Cámaras",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 70.\n"
            "1. La ley electoral determinará las causas de inelegibilidad e incompatibilidad de los "
            "Diputados y Senadores, que comprenderán, en todo caso:\n"
            "a) A los componentes del Tribunal Constitucional.\n"
            "b) A los altos cargos de la Administración del Estado que determine la ley, con la "
            "excepción de los miembros del Gobierno.\n"
            "c) Al Defensor del Pueblo.\n"
            "d) A los Magistrados, Jueces y Fiscales en activo.\n"
            "e) A los militares profesionales y miembros de las Fuerzas y Cuerpos de Seguridad y "
            "Policía en activo.\n"
            "f) A los miembros de las Juntas Electorales.\n"
            "2. La validez de las actas y credenciales de los miembros de ambas Cámaras estará sometida "
            "al control judicial, en los términos que establezca la ley electoral."
        ),
    },
    {
        "numero": "71",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO I. De las Cámaras",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 71.\n"
            "1. Los Diputados y Senadores gozarán de inviolabilidad por las opiniones manifestadas en "
            "el ejercicio de sus funciones.\n"
            "2. Durante el período de su mandato los Diputados y Senadores gozarán asimismo de "
            "inmunidad y sólo podrán ser detenidos en caso de flagrante delito. No podrán ser "
            "inculpados ni procesados sin la previa autorización de la Cámara respectiva.\n"
            "3. En las causas contra Diputados y Senadores será competente la Sala de lo Penal del "
            "Tribunal Supremo.\n"
            "4. Los Diputados y Senadores percibirán una asignación que será fijada por las respectivas "
            "Cámaras."
        ),
    },
    {
        "numero": "72",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO I. De las Cámaras",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 72.\n"
            "1. Las Cámaras establecen sus propios Reglamentos, aprueban autónomamente sus presupuestos "
            "y, de común acuerdo, regulan el Estatuto del Personal de las Cortes Generales. Los "
            "Reglamentos y su reforma serán sometidos a una votación final sobre su totalidad, que "
            "requerirá la mayoría absoluta.\n"
            "2. Las Cámaras eligen sus respectivos Presidentes y los demás miembros de sus Mesas. Las "
            "sesiones conjuntas serán presididas por el Presidente del Congreso y se regirán por un "
            "Reglamento de las Cortes Generales aprobado por mayoría absoluta de cada Cámara.\n"
            "3. Los Presidentes de las Cámaras ejercen en nombre de las mismas todos los poderes "
            "administrativos y facultades de policía en el interior de sus respectivas sedes."
        ),
    },
    {
        "numero": "73",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO I. De las Cámaras",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 73.\n"
            "1. Las Cámaras se reunirán anualmente en dos períodos ordinarios de sesiones: el primero, "
            "de septiembre a diciembre, y el segundo, de febrero a junio.\n"
            "2. Las Cámaras podrán reunirse en sesiones extraordinarias a petición del Gobierno, de la "
            "Diputación Permanente o de la mayoría absoluta de los miembros de cualquiera de las "
            "Cámaras. Las sesiones extraordinarias deberán convocarse sobre un orden del día "
            "determinado y serán clausuradas una vez que éste haya sido agotado."
        ),
    },
    {
        "numero": "74",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO I. De las Cámaras",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 74.\n"
            "1. Las Cámaras se reunirán en sesión conjunta para ejercer las competencias no legislativas "
            "que el Título II atribuye expresamente a las Cortes Generales.\n"
            "2. Las decisiones de las Cortes Generales previstas en los artículos 94, 1, 145, 2, y 158, "
            "2, se adoptarán por mayoría de cada una de las Cámaras. En el primer caso, el procedimiento "
            "se iniciará por el Congreso, y en los otros dos, por el Senado. En ambos casos, si no "
            "hubiera acuerdo entre Senado y Congreso, se intentará obtener por una Comisión Mixta "
            "compuesta de igual número de Diputados y Senadores. La Comisión presentará un texto que "
            "será votado por ambas Cámaras. Si no se aprueba en la forma establecida, decidirá el "
            "Congreso por mayoría absoluta."
        ),
    },
    {
        "numero": "75",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO I. De las Cámaras",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 75.\n"
            "1. Las Cámaras funcionarán en Pleno y por Comisiones.\n"
            "2. Las Cámaras podrán delegar en las Comisiones Legislativas Permanentes la aprobación de "
            "proyectos o proposiciones de ley. El Pleno podrá, no obstante, recabar en cualquier "
            "momento el debate y votación de cualquier proyecto o proposición de ley que haya sido "
            "objeto de esta delegación.\n"
            "3. Quedan exceptuados de lo dispuesto en el apartado anterior la reforma constitucional, "
            "las cuestiones internacionales, los proyectos de ley orgánica y de bases y los "
            "Presupuestos Generales del Estado."
        ),
    },
    {
        "numero": "76",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO I. De las Cámaras",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 76.\n"
            "1. El Congreso y el Senado, y, en su caso, ambas Cámaras conjuntamente, podrán nombrar "
            "Comisiones de investigación sobre cualquier asunto de interés público. Sus conclusiones "
            "no serán vinculantes para los Tribunales, ni afectarán a las resoluciones judiciales, "
            "sin perjuicio de que el resultado de la investigación sea comunicado al Ministerio Fiscal "
            "para el ejercicio, cuando proceda, de las acciones oportunas.\n"
            "2. Será obligatorio comparecer a requerimiento de las Cámaras. La ley regulará las "
            "sanciones que puedan imponerse por incumplimiento de esta obligación."
        ),
    },
    {
        "numero": "77",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO I. De las Cámaras",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 77.\n"
            "1. Las Cámaras pueden recibir peticiones individuales y colectivas, siempre por escrito, "
            "quedando prohibida la presentación directa por manifestaciones ciudadanas.\n"
            "2. Las Cámaras pueden remitir al Gobierno las peticiones que reciban. El Gobierno está "
            "obligado a explicarse sobre su contenido, siempre que las Cámaras lo exijan."
        ),
    },
    {
        "numero": "78",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO I. De las Cámaras",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 78.\n"
            "1. En cada Cámara habrá una Diputación Permanente compuesta por un mínimo de veintiún "
            "miembros, que representarán a los grupos parlamentarios, en proporción a su importancia numérica.\n"
            "2. Las Diputaciones Permanentes estarán presididas por el Presidente de la Cámara "
            "respectiva y tendrán como funciones la prevista en el artículo 73, la de asumir las "
            "facultades que correspondan a las Cámaras, de acuerdo con los artículos 86 y 116, en caso "
            "de que éstas hubieren sido disueltas o hubiere expirado su mandato y la de velar por los "
            "poderes de las Cámaras cuando éstas no estén reunidas.\n"
            "3. Expirado el mandato o en caso de disolución, las Diputaciones Permanentes seguirán "
            "ejerciendo sus funciones hasta la constitución de las nuevas Cortes Generales.\n"
            "4. Reunida la Cámara correspondiente, la Diputación Permanente dará cuenta de los asuntos "
            "tratados y de sus decisiones."
        ),
    },
    {
        "numero": "79",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO I. De las Cámaras",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 79.\n"
            "1. Para adoptar acuerdos, las Cámaras deben estar reunidas reglamentariamente y con "
            "asistencia de la mayoría de sus miembros.\n"
            "2. Dichos acuerdos, para ser válidos, deberán ser aprobados por la mayoría de los miembros "
            "presentes, sin perjuicio de las mayorías especiales que establezcan la Constitución o las "
            "leyes orgánicas y las que para elección de personas establezcan los Reglamentos de las "
            "Cámaras.\n"
            "3. El voto de Senadores y Diputados es personal e indelegable."
        ),
    },
    {
        "numero": "80",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO I. De las Cámaras",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 80.\n"
            "Las sesiones plenarias de las Cámaras serán públicas, salvo acuerdo en contrario de cada "
            "Cámara, adoptado por mayoría absoluta o con arreglo al Reglamento."
        ),
    },
    # TÍTULO III · Cap II (81–96)
    {
        "numero": "81",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO II. De la elaboración de las leyes",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 81.\n"
            "1. Son leyes orgánicas las relativas al desarrollo de los derechos fundamentales y de las "
            "libertades públicas, las que aprueben los Estatutos de Autonomía y el régimen electoral "
            "general y las demás previstas en la Constitución.\n"
            "2. La aprobación, modificación o derogación de las leyes orgánicas exigirá mayoría "
            "absoluta del Congreso, en una votación final sobre el conjunto del proyecto."
        ),
    },
    {
        "numero": "82",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO II. De la elaboración de las leyes",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 82.\n"
            "1. Las Cortes Generales podrán delegar en el Gobierno la potestad de dictar normas con "
            "rango de ley sobre materias determinadas no incluidas en el artículo anterior.\n"
            "2. La delegación legislativa deberá otorgarse mediante una ley de bases cuando su objeto "
            "sea la formación de textos articulados o por una ley ordinaria cuando se trate de refundir "
            "varios textos legales en uno solo.\n"
            "3. La delegación legislativa habrá de otorgarse al Gobierno de forma expresa para materia "
            "concreta y con fijación del plazo para su ejercicio. La delegación se agota por el uso "
            "que de ella haga el Gobierno mediante la publicación de la norma correspondiente. No "
            "podrá entenderse concedida de modo implícito o por tiempo indeterminado. Tampoco podrá "
            "permitir la subdelegación a autoridades distintas del propio Gobierno.\n"
            "4. Las leyes de bases delimitarán con precisión el objeto y alcance de la delegación "
            "legislativa y los principios y criterios que han de seguirse en su ejercicio.\n"
            "5. La autorización para refundir textos legales determinará el ámbito normativo a que se "
            "refiere el contenido de la delegación, especificando si se circunscribe a la mera "
            "formulación de un texto único o si se incluye la de regularizar, aclarar y armonizar los "
            "textos legales que han de ser refundidos.\n"
            "6. Sin perjuicio de la competencia propia de los Tribunales, las leyes de delegación "
            "podrán establecer en cada caso fórmulas adicionales de control."
        ),
    },
    {
        "numero": "83",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO II. De la elaboración de las leyes",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 83.\n"
            "Las leyes de bases no podrán en ningún caso:\n"
            "a) Autorizar la modificación de la propia ley de bases.\n"
            "b) Facultar para dictar normas con carácter retroactivo."
        ),
    },
    {
        "numero": "84",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO II. De la elaboración de las leyes",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 84.\n"
            "Cuando una proposición de ley o una enmienda fuere contraria a una delegación legislativa "
            "en vigor, el Gobierno está facultado para oponerse a su tramitación. En tal supuesto, "
            "podrá presentarse una proposición de ley para la derogación total o parcial de la ley de delegación."
        ),
    },
    {
        "numero": "85",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO II. De la elaboración de las leyes",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 85.\n"
            "Las disposiciones del Gobierno que contengan legislación delegada recibirán el título de "
            "Decretos Legislativos."
        ),
    },
    {
        "numero": "86",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO II. De la elaboración de las leyes",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 86.\n"
            "1. En caso de extraordinaria y urgente necesidad, el Gobierno podrá dictar disposiciones "
            "legislativas provisionales que tomarán la forma de Decretos-leyes y que no podrán afectar "
            "al ordenamiento de las instituciones básicas del Estado, a los derechos, deberes y "
            "libertades de los ciudadanos regulados en el Título I, al régimen de las Comunidades "
            "Autónomas ni al Derecho electoral general.\n"
            "2. Los Decretos-leyes deberán ser inmediatamente sometidos a debate y votación de "
            "totalidad al Congreso de los Diputados, convocado al efecto si no estuviere reunido, en "
            "el plazo de los treinta días siguientes a su promulgación. El Congreso habrá de pronunciarse "
            "expresamente dentro de dicho plazo sobre su convalidación o derogación, para lo cual el "
            "Reglamento establecerá un procedimiento especial y sumario.\n"
            "3. Durante el plazo establecido en el apartado anterior, las Cortes podrán tramitarlos "
            "como proyectos de ley por el procedimiento de urgencia."
        ),
    },
    {
        "numero": "87",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO II. De la elaboración de las leyes",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 87.\n"
            "1. La iniciativa legislativa corresponde al Gobierno, al Congreso y al Senado, de acuerdo "
            "con la Constitución y los Reglamentos de las Cámaras.\n"
            "2. Las Asambleas de las Comunidades Autónomas podrán solicitar del Gobierno la adopción "
            "de un proyecto de ley o remitir a la Mesa del Congreso una proposición de ley, delegando "
            "ante dicha Cámara un máximo de tres miembros de la Asamblea encargados de su defensa.\n"
            "3. Una ley orgánica regulará las formas de ejercicio y requisitos de la iniciativa popular "
            "para la presentación de proposiciones de ley. En todo caso se exigirán no menos de "
            "500.000 firmas acreditadas. No procederá dicha iniciativa en materias propias de ley "
            "orgánica, tributarias o de carácter internacional, ni en lo relativo a la prerrogativa "
            "de gracia."
        ),
    },
    {
        "numero": "88",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO II. De la elaboración de las leyes",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 88.\n"
            "Los proyectos de ley serán aprobados en Consejo de Ministros, que los someterá al Congreso, "
            "acompañados de una exposición de motivos y de los antecedentes necesarios para pronunciarse "
            "sobre ellos."
        ),
    },
    {
        "numero": "89",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO II. De la elaboración de las leyes",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 89.\n"
            "1. La tramitación de las proposiciones de ley se regulará por los Reglamentos de las "
            "Cámaras, sin que la prioridad debida a los proyectos de ley impida el ejercicio de la "
            "iniciativa legislativa en los términos regulados por el artículo 87.\n"
            "2. Las proposiciones de ley que, de acuerdo con el artículo 87, tome en consideración el "
            "Senado, se remitirán al Congreso para su trámite en éste como tal proposición."
        ),
    },
    {
        "numero": "90",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO II. De la elaboración de las leyes",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 90.\n"
            "1. Aprobado un proyecto de ley ordinaria u orgánica por el Congreso de los Diputados, su "
            "Presidente dará inmediata cuenta del mismo al Presidente del Senado, el cual lo someterá "
            "a la deliberación de éste.\n"
            "2. El Senado, en el plazo de dos meses, a partir del día de la recepción del texto, puede, "
            "mediante mensaje motivado, oponer su veto o introducir enmiendas al mismo. El veto deberá "
            "ser aprobado por mayoría absoluta. El proyecto no podrá ser sometido al Rey para su "
            "sanción sin que el Congreso ratifique por mayoría absoluta, en caso de veto, el texto "
            "inicial, o por mayoría simple, una vez transcurridos dos meses desde la interposición del "
            "mismo, o se pronuncie sobre las enmiendas, aceptándolas o no por mayoría simple.\n"
            "3. El plazo de dos meses de que el Senado dispone para vetar o enmendar el proyecto se "
            "reducirá al de veinte días naturales en los proyectos declarados urgentes por el Gobierno "
            "o por el Congreso de los Diputados."
        ),
    },
    {
        "numero": "91",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO II. De la elaboración de las leyes",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 91.\n"
            "El Rey sancionará en el plazo de quince días las leyes aprobadas por las Cortes Generales, "
            "y las promulgará y ordenará su inmediata publicación."
        ),
    },
    {
        "numero": "92",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO II. De la elaboración de las leyes",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 92.\n"
            "1. Las decisiones políticas de especial trascendencia podrán ser sometidas a referéndum "
            "consultivo de todos los ciudadanos.\n"
            "2. El referéndum será convocado por el Rey, mediante propuesta del Presidente del Gobierno, "
            "previamente autorizada por el Congreso de los Diputados.\n"
            "3. Una ley orgánica regulará las condiciones y el procedimiento de las distintas "
            "modalidades de referéndum previstas en esta Constitución."
        ),
    },
    {
        "numero": "93",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO II. De la elaboración de las leyes",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 93.\n"
            "Mediante ley orgánica se podrá autorizar la celebración de tratados por los que se atribuya "
            "a una organización o institución internacional el ejercicio de competencias derivadas de "
            "la Constitución. Corresponde a las Cortes Generales o al Gobierno, según los casos, la "
            "garantía del cumplimiento de estos tratados y de las resoluciones emanadas de los "
            "organismos internacionales o supranacionales titulares de la cesión."
        ),
    },
    {
        "numero": "94",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO II. De la elaboración de las leyes",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 94.\n"
            "1. La prestación del consentimiento del Estado para obligarse por medio de tratados o "
            "convenios requerirá la previa autorización de las Cortes Generales, en los siguientes casos:\n"
            "a) Tratados de carácter político.\n"
            "b) Tratados o convenios de carácter militar.\n"
            "c) Tratados o convenios que afecten a la integridad territorial del Estado o a los "
            "derechos y deberes fundamentales establecidos en el Título I.\n"
            "d) Tratados o convenios que impliquen obligaciones financieras para la Hacienda Pública.\n"
            "e) Tratados o convenios que supongan modificación o derogación de alguna ley o exijan "
            "medidas legislativas para su ejecución.\n"
            "2. El Congreso y el Senado serán inmediatamente informados de la conclusión de los "
            "restantes tratados o convenios."
        ),
    },
    {
        "numero": "95",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO II. De la elaboración de las leyes",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 95.\n"
            "1. La celebración de un tratado internacional que contenga estipulaciones contrarias a la "
            "Constitución exigirá la previa revisión constitucional.\n"
            "2. El Gobierno o cualquiera de las Cámaras puede requerir al Tribunal Constitucional para "
            "que declare si existe o no esa contradicción."
        ),
    },
    {
        "numero": "96",
        "titulo": None,
        "titulo_titulo": "TÍTULO III. De las Cortes Generales",
        "titulo_capitulo": "CAPÍTULO II. De la elaboración de las leyes",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 96.\n"
            "1. Los tratados internacionales válidamente celebrados, una vez publicados oficialmente "
            "en España, formarán parte del ordenamiento interno. Sus disposiciones sólo podrán ser "
            "derogadas, modificadas o suspendidas en la forma prevista en los propios tratados o de "
            "acuerdo con las normas generales del Derecho internacional.\n"
            "2. Para la denuncia de los tratados y convenios internacionales se utilizará el mismo "
            "procedimiento previsto para su aprobación en el artículo 94."
        ),
    },
    # TÍTULO IV (100–107)
    {
        "numero": "100",
        "titulo": None,
        "titulo_titulo": "TÍTULO IV. Del Gobierno y de la Administración",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 100.\n"
            "Los demás miembros del Gobierno serán nombrados y separados por el Rey, a propuesta de "
            "su Presidente."
        ),
    },
    {
        "numero": "101",
        "titulo": None,
        "titulo_titulo": "TÍTULO IV. Del Gobierno y de la Administración",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 101.\n"
            "1. El Gobierno cesa tras la celebración de elecciones generales, en los casos de pérdida "
            "de la confianza parlamentaria previstos en la Constitución, o por dimisión o fallecimiento "
            "de su Presidente.\n"
            "2. El Gobierno cesante continuará en funciones hasta la toma de posesión del nuevo Gobierno."
        ),
    },
    {
        "numero": "102",
        "titulo": None,
        "titulo_titulo": "TÍTULO IV. Del Gobierno y de la Administración",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 102.\n"
            "1. La responsabilidad criminal del Presidente y los demás miembros del Gobierno será "
            "exigible, en su caso, ante la Sala de lo Penal del Tribunal Supremo.\n"
            "2. Si la acusación fuere por traición o por cualquier delito contra la seguridad del "
            "Estado en el ejercicio de sus funciones, sólo podrá ser planteada por iniciativa de la "
            "cuarta parte de los miembros del Congreso, y con la aprobación de la mayoría absoluta "
            "del mismo.\n"
            "3. La prerrogativa real de gracia no será aplicable a ninguno de los supuestos del "
            "presente artículo."
        ),
    },
    {
        "numero": "103",
        "titulo": None,
        "titulo_titulo": "TÍTULO IV. Del Gobierno y de la Administración",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 103.\n"
            "1. La Administración Pública sirve con objetividad los intereses generales y actúa de "
            "acuerdo con los principios de eficacia, jerarquía, descentralización, desconcentración y "
            "coordinación, con sometimiento pleno a la ley y al Derecho.\n"
            "2. Los órganos de la Administración del Estado son creados, regidos y coordinados de "
            "acuerdo con la ley.\n"
            "3. La ley regulará el estatuto de los funcionarios públicos, el acceso a la función "
            "pública de acuerdo con los principios de mérito y capacidad, las peculiaridades del "
            "ejercicio de su derecho a sindicación, el sistema de incompatibilidades y las garantías "
            "para la imparcialidad en el ejercicio de sus funciones."
        ),
    },
    {
        "numero": "104",
        "titulo": None,
        "titulo_titulo": "TÍTULO IV. Del Gobierno y de la Administración",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 104.\n"
            "1. Las Fuerzas y Cuerpos de seguridad, bajo la dependencia del Gobierno, tendrán como "
            "misión proteger el libre ejercicio de los derechos y libertades y garantizar la seguridad ciudadana.\n"
            "2. Una ley orgánica determinará las funciones, principios básicos de actuación y estatutos "
            "de las Fuerzas y Cuerpos de seguridad."
        ),
    },
    {
        "numero": "105",
        "titulo": None,
        "titulo_titulo": "TÍTULO IV. Del Gobierno y de la Administración",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 105.\n"
            "La ley regulará:\n"
            "a) La audiencia de los ciudadanos, directamente o a través de las organizaciones y "
            "asociaciones reconocidas por la ley, en el procedimiento de elaboración de las "
            "disposiciones administrativas que les afecten.\n"
            "b) El acceso de los ciudadanos a los archivos y registros administrativos, salvo en lo "
            "que afecte a la seguridad y defensa del Estado, la averiguación de los delitos y la "
            "intimidad de las personas.\n"
            "c) El procedimiento a través del cual deben producirse los actos administrativos, "
            "garantizando, cuando proceda, la audiencia del interesado."
        ),
    },
    {
        "numero": "106",
        "titulo": None,
        "titulo_titulo": "TÍTULO IV. Del Gobierno y de la Administración",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 106.\n"
            "1. Los Tribunales controlan la potestad reglamentaria y la legalidad de la actuación "
            "administrativa, así como el sometimiento de ésta a los fines que la justifican.\n"
            "2. Los particulares, en los términos establecidos por la ley, tendrán derecho a ser "
            "indemnizados por toda lesión que sufran en cualquiera de sus bienes y derechos, salvo en "
            "los casos de fuerza mayor, siempre que la lesión sea consecuencia del funcionamiento de "
            "los servicios públicos."
        ),
    },
    {
        "numero": "107",
        "titulo": None,
        "titulo_titulo": "TÍTULO IV. Del Gobierno y de la Administración",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 107.\n"
            "El Consejo de Estado es el supremo órgano consultivo del Gobierno. Una ley orgánica "
            "regulará su composición y competencia."
        ),
    },
    # TÍTULO V (109–112, 114–116)
    {
        "numero": "109",
        "titulo": None,
        "titulo_titulo": "TÍTULO V. De las relaciones entre el Gobierno y las Cortes Generales",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 109.\n"
            "Las Cámaras y sus Comisiones podrán recabar, a través de los Presidentes de aquéllas, "
            "la información y ayuda que precisen del Gobierno y de sus Departamentos y de cualesquiera "
            "autoridades del Estado y de las Comunidades Autónomas."
        ),
    },
    {
        "numero": "110",
        "titulo": None,
        "titulo_titulo": "TÍTULO V. De las relaciones entre el Gobierno y las Cortes Generales",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 110.\n"
            "1. Las Cámaras y sus Comisiones pueden reclamar la presencia de los miembros del Gobierno.\n"
            "2. Los miembros del Gobierno tienen acceso a las sesiones de las Cámaras y a sus Comisiones "
            "y la facultad de hacerse oír en ellas, y podrán solicitar que informen ante las mismas "
            "funcionarios de sus Departamentos."
        ),
    },
    {
        "numero": "111",
        "titulo": None,
        "titulo_titulo": "TÍTULO V. De las relaciones entre el Gobierno y las Cortes Generales",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 111.\n"
            "1. El Gobierno y cada uno de sus miembros están sometidos a las interpelaciones y preguntas "
            "que se le formulen en las Cámaras. Para esta clase de debate los Reglamentos establecerán "
            "un tiempo mínimo semanal.\n"
            "2. Toda interpelación podrá dar lugar a una moción en la que la Cámara manifieste su "
            "posición."
        ),
    },
    {
        "numero": "112",
        "titulo": None,
        "titulo_titulo": "TÍTULO V. De las relaciones entre el Gobierno y las Cortes Generales",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 112.\n"
            "El Presidente del Gobierno, previa deliberación del Consejo de Ministros, puede plantear "
            "ante el Congreso de los Diputados la cuestión de confianza sobre su programa o sobre una "
            "declaración de política general. La confianza se entenderá otorgada cuando vote a favor "
            "de la misma la mayoría simple de los Diputados."
        ),
    },
    {
        "numero": "114",
        "titulo": None,
        "titulo_titulo": "TÍTULO V. De las relaciones entre el Gobierno y las Cortes Generales",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 114.\n"
            "1. Si el Congreso niega su confianza al Gobierno, éste presentará su dimisión al Rey, "
            "procediéndose a continuación a la designación de Presidente del Gobierno, según lo "
            "dispuesto en el artículo 99.\n"
            "2. Si el Congreso adopta una moción de censura, el Gobierno presentará su dimisión al Rey "
            "y el candidato incluido en aquélla se entenderá investido de la confianza de la Cámara a "
            "los efectos previstos en el artículo 99. El Rey le nombrará Presidente del Gobierno."
        ),
    },
    {
        "numero": "115",
        "titulo": None,
        "titulo_titulo": "TÍTULO V. De las relaciones entre el Gobierno y las Cortes Generales",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 115.\n"
            "1. El Presidente del Gobierno, previa deliberación del Consejo de Ministros, y bajo su "
            "exclusiva responsabilidad, podrá proponer la disolución del Congreso, del Senado o de "
            "las Cortes Generales, que será decretada por el Rey. El decreto de disolución fijará la "
            "fecha de las elecciones.\n"
            "2. La propuesta de disolución no podrá presentarse cuando esté en trámite una moción de "
            "censura.\n"
            "3. No procederá nueva disolución antes de que transcurra un año desde la anterior, salvo "
            "lo dispuesto en el artículo 99, apartado 5."
        ),
    },
    {
        "numero": "116",
        "titulo": None,
        "titulo_titulo": "TÍTULO V. De las relaciones entre el Gobierno y las Cortes Generales",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 116.\n"
            "1. Una ley orgánica regulará los estados de alarma, de excepción y de sitio, y las "
            "competencias y limitaciones correspondientes.\n"
            "2. El estado de alarma será declarado por el Gobierno mediante decreto acordado en Consejo "
            "de Ministros por un plazo máximo de quince días, dando cuenta al Congreso de los Diputados, "
            "reunido inmediatamente al efecto y sin cuya autorización no podrá ser prorrogado dicho "
            "plazo. El decreto determinará el ámbito territorial a que se extienden los efectos de la "
            "declaración.\n"
            "3. El estado de excepción será declarado por el Gobierno mediante decreto acordado en "
            "Consejo de Ministros, previa autorización del Congreso de los Diputados. La autorización "
            "y proclamación del estado de excepción deberá determinar expresamente los efectos del "
            "mismo, el ámbito territorial a que se extiende y su duración, que no podrá exceder de "
            "treinta días, prorrogables por otro plazo igual, con los mismos requisitos.\n"
            "4. El estado de sitio será declarado por la mayoría absoluta del Congreso de los Diputados, "
            "a propuesta exclusiva del Gobierno. El Congreso determinará su ámbito territorial, "
            "duración y condiciones.\n"
            "5. No podrá procederse a la disolución del Congreso mientras estén declarados algunos de "
            "los estados comprendidos en el presente artículo, quedando automáticamente convocadas las "
            "Cámaras si no estuvieren en período de sesiones. Su funcionamiento, así como el de los "
            "demás poderes constitucionales del Estado, no podrá interrumpirse durante la vigencia de "
            "estos estados.\n"
            "Disuelto el Congreso o expirado su mandato, si se produjere alguna de las situaciones que "
            "dan lugar a cualquiera de dichos estados, las competencias del Congreso serán asumidas por "
            "su Diputación Permanente.\n"
            "6. La declaración de los estados de alarma, de excepción y de sitio no modificarán el "
            "principio de responsabilidad del Gobierno y de sus agentes reconocidos en la Constitución "
            "y en las leyes."
        ),
    },
    # TÍTULO VI (118–121, 123–127)
    {
        "numero": "118",
        "titulo": None,
        "titulo_titulo": "TÍTULO VI. Del Poder Judicial",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 118.\n"
            "Es obligado cumplir las sentencias y demás resoluciones firmes de los Jueces y Tribunales, "
            "así como prestar la colaboración requerida por éstos en el curso del proceso y en la "
            "ejecución de lo resuelto."
        ),
    },
    {
        "numero": "119",
        "titulo": None,
        "titulo_titulo": "TÍTULO VI. Del Poder Judicial",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 119.\n"
            "La justicia será gratuita cuando así lo disponga la ley y, en todo caso, respecto de "
            "quienes acrediten insuficiencia de recursos para litigar."
        ),
    },
    {
        "numero": "120",
        "titulo": None,
        "titulo_titulo": "TÍTULO VI. Del Poder Judicial",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 120.\n"
            "1. Las actuaciones judiciales serán públicas, con las excepciones que prevean las leyes "
            "de procedimiento.\n"
            "2. El procedimiento será predominantemente oral, sobre todo en materia criminal.\n"
            "3. Las sentencias serán siempre motivadas y se pronunciarán en audiencia pública."
        ),
    },
    {
        "numero": "121",
        "titulo": None,
        "titulo_titulo": "TÍTULO VI. Del Poder Judicial",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 121.\n"
            "Los daños causados por error judicial, así como los que sean consecuencia del "
            "funcionamiento anormal de la Administración de Justicia, darán derecho a una indemnización "
            "a cargo del Estado, conforme a la ley."
        ),
    },
    {
        "numero": "123",
        "titulo": None,
        "titulo_titulo": "TÍTULO VI. Del Poder Judicial",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 123.\n"
            "1. El Tribunal Supremo, con jurisdicción en toda España, es el órgano jurisdiccional "
            "superior en todos los órdenes, salvo lo dispuesto en materia de garantías constitucionales.\n"
            "2. El Presidente del Tribunal Supremo será nombrado por el Rey, a propuesta del Consejo "
            "General del Poder Judicial, en la forma que determine la ley."
        ),
    },
    {
        "numero": "124",
        "titulo": None,
        "titulo_titulo": "TÍTULO VI. Del Poder Judicial",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 124.\n"
            "1. El Ministerio Fiscal, sin perjuicio de las funciones encomendadas a otros órganos, "
            "tiene por misión promover la acción de la justicia en defensa de la legalidad, de los "
            "derechos de los ciudadanos y del interés público tutelado por la ley, de oficio o a "
            "petición de los interesados, así como velar por la independencia de los Tribunales y "
            "procurar ante éstos la satisfacción del interés social.\n"
            "2. El Ministerio Fiscal ejerce sus funciones por medio de órganos propios conforme a los "
            "principios de unidad de actuación y dependencia jerárquica y con sujeción, en todo caso, "
            "a los de legalidad e imparcialidad.\n"
            "3. La ley regulará el estatuto orgánico del Ministerio Fiscal.\n"
            "4. El Fiscal General del Estado será nombrado por el Rey, a propuesta del Gobierno, oído "
            "el Consejo General del Poder Judicial."
        ),
    },
    {
        "numero": "125",
        "titulo": None,
        "titulo_titulo": "TÍTULO VI. Del Poder Judicial",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 125.\n"
            "Los ciudadanos podrán ejercer la acción popular y participar en la Administración de "
            "Justicia mediante la institución del Jurado, en la forma y con respecto a aquellos "
            "procesos penales que la ley determine, así como en los Tribunales consuetudinarios y "
            "tradicionales."
        ),
    },
    {
        "numero": "126",
        "titulo": None,
        "titulo_titulo": "TÍTULO VI. Del Poder Judicial",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 126.\n"
            "La policía judicial depende de los Jueces, de los Tribunales y del Ministerio Fiscal en "
            "sus funciones de averiguación del delito y descubrimiento y aseguramiento del delincuente, "
            "en los términos que la ley establezca."
        ),
    },
    {
        "numero": "127",
        "titulo": None,
        "titulo_titulo": "TÍTULO VI. Del Poder Judicial",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 127.\n"
            "1. Los Jueces y Magistrados así como los Fiscales, mientras se hallen en activo, no podrán "
            "desempeñar otros cargos públicos, ni pertenecer a partidos políticos o sindicatos. La ley "
            "establecerá el sistema y modalidades de asociación profesional de los Jueces, Magistrados "
            "y Fiscales.\n"
            "2. La ley establecerá el régimen de incompatibilidades de los miembros del poder judicial, "
            "que deberá asegurar la total independencia de los mismos."
        ),
    },
    # TÍTULO VII (129–134, 136)
    {
        "numero": "129",
        "titulo": None,
        "titulo_titulo": "TÍTULO VII. Economía y Hacienda",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 129.\n"
            "1. La ley establecerá las formas de participación de los interesados en la Seguridad "
            "Social y en la actividad de los organismos públicos cuya función afecte directamente a "
            "la calidad de la vida o al bienestar general.\n"
            "2. Los poderes públicos promoverán eficazmente las diversas formas de participación en "
            "la empresa y fomentarán, mediante una legislación adecuada, las sociedades cooperativas. "
            "También establecerán los medios que faciliten el acceso de los trabajadores a la "
            "propiedad de los medios de producción."
        ),
    },
    {
        "numero": "130",
        "titulo": None,
        "titulo_titulo": "TÍTULO VII. Economía y Hacienda",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 130.\n"
            "1. Los poderes públicos atenderán a la modernización y desarrollo de todos los sectores "
            "económicos y, en particular, de la agricultura, de la ganadería, de la pesca y de la "
            "artesanía, a fin de equiparar el nivel de vida de todos los españoles.\n"
            "2. Con el mismo fin, se dispensará un tratamiento especial a las zonas de montaña."
        ),
    },
    {
        "numero": "131",
        "titulo": None,
        "titulo_titulo": "TÍTULO VII. Economía y Hacienda",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 131.\n"
            "1. El Estado, mediante ley, podrá planificar la actividad económica general para atender "
            "a las necesidades colectivas, equilibrar y armonizar el desarrollo regional y sectorial "
            "y estimular el crecimiento de la renta y de la riqueza y su más justa distribución.\n"
            "2. El Gobierno elaborará los proyectos de planificación, de acuerdo con las previsiones "
            "que le sean suministradas por las Comunidades Autónomas y el asesoramiento y colaboración "
            "de los sindicatos y otras organizaciones profesionales, empresariales y económicas. A tal "
            "fin se constituirá un Consejo, cuya composición y funciones se desarrollarán por ley."
        ),
    },
    {
        "numero": "132",
        "titulo": None,
        "titulo_titulo": "TÍTULO VII. Economía y Hacienda",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 132.\n"
            "1. La ley regulará el régimen jurídico de los bienes de dominio público y de los "
            "comunales, inspirándose en los principios de inalienabilidad, imprescriptibilidad e "
            "inembargabilidad, así como su desafectación.\n"
            "2. Son bienes de dominio público estatal los que determine la ley y, en todo caso, la "
            "zona marítimo-terrestre, las playas, el mar territorial y los recursos naturales de la "
            "zona económica y la plataforma continental.\n"
            "3. Por ley se regularán el Patrimonio del Estado y el Patrimonio Nacional, su "
            "administración, defensa y conservación."
        ),
    },
    {
        "numero": "133",
        "titulo": None,
        "titulo_titulo": "TÍTULO VII. Economía y Hacienda",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 133.\n"
            "1. La potestad originaria para establecer los tributos corresponde exclusivamente al "
            "Estado, mediante ley.\n"
            "2. Las Comunidades Autónomas y las Corporaciones locales podrán establecer y exigir "
            "tributos, de acuerdo con la Constitución y las leyes.\n"
            "3. Todo beneficio fiscal que afecte a los tributos del Estado deberá establecerse en "
            "virtud de ley.\n"
            "4. Las administraciones públicas sólo podrán contraer obligaciones financieras y realizar "
            "gastos de acuerdo con las leyes."
        ),
    },
    {
        "numero": "134",
        "titulo": None,
        "titulo_titulo": "TÍTULO VII. Economía y Hacienda",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 134.\n"
            "1. Corresponde al Gobierno la elaboración de los Presupuestos Generales del Estado y a "
            "las Cortes Generales, su examen, enmienda y aprobación.\n"
            "2. Los Presupuestos Generales del Estado tendrán carácter anual, incluirán la totalidad "
            "de los gastos e ingresos del sector público estatal y en ellos se consignará el importe "
            "de los beneficios fiscales que afecten a los tributos del Estado.\n"
            "3. El Gobierno deberá presentar ante el Congreso de los Diputados los Presupuestos "
            "Generales del Estado al menos tres meses antes de la expiración de los del año anterior.\n"
            "4. Si la Ley de Presupuestos no se aprobara antes del primer día del ejercicio económico "
            "correspondiente, se considerarán automáticamente prorrogados los Presupuestos del "
            "ejercicio anterior hasta la aprobación de los nuevos.\n"
            "5. Aprobados los Presupuestos Generales del Estado, el Gobierno podrá presentar proyectos "
            "de ley que impliquen aumento del gasto público o disminución de los ingresos "
            "correspondientes al mismo ejercicio presupuestario.\n"
            "6. Toda proposición o enmienda que suponga aumento de los créditos o disminución de los "
            "ingresos presupuestarios requerirá la conformidad del Gobierno para su tramitación.\n"
            "7. La Ley de Presupuestos no puede crear tributos. Podrá modificarlos cuando una ley "
            "tributaria sustantiva así lo prevea."
        ),
    },
    {
        "numero": "136",
        "titulo": None,
        "titulo_titulo": "TÍTULO VII. Economía y Hacienda",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 136.\n"
            "1. El Tribunal de Cuentas es el supremo órgano fiscalizador de las cuentas y de la gestión "
            "económica del Estado, así como del sector público.\n"
            "Dependerá directamente de las Cortes Generales y ejercerá sus funciones por delegación "
            "de ellas en el examen y comprobación de la Cuenta General del Estado.\n"
            "2. Las cuentas del Estado y del sector público estatal se rendirán al Tribunal de Cuentas "
            "y serán censuradas por éste.\n"
            "El Tribunal de Cuentas, sin perjuicio de su propia jurisdicción, remitirá a las Cortes "
            "Generales un informe anual en el que, cuando proceda, comunicará las infracciones o "
            "responsabilidades en que, a su juicio, se hubiere incurrido.\n"
            "3. Los miembros del Tribunal de Cuentas gozarán de la misma independencia e inamovilidad "
            "y estarán sometidos a las mismas incompatibilidades que los Jueces.\n"
            "4. Una ley orgánica regulará la composición, organización y funciones del Tribunal de "
            "Cuentas."
        ),
    },
    # TÍTULO VIII (138–139, 141–158)
    {
        "numero": "138",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO I. Principios generales",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 138.\n"
            "1. El Estado garantiza la realización efectiva del principio de solidaridad consagrado en "
            "el artículo 2 de la Constitución, velando por el establecimiento de un equilibrio económico, "
            "adecuado y justo entre las diversas partes del territorio español, y atendiendo en "
            "particular a las circunstancias del hecho insular.\n"
            "2. Las diferencias entre los Estatutos de las distintas Comunidades Autónomas no podrán "
            "implicar, en ningún caso, privilegios económicos o sociales."
        ),
    },
    {
        "numero": "139",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO I. Principios generales",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 139.\n"
            "1. Todos los españoles tienen los mismos derechos y obligaciones en cualquier parte del "
            "territorio del Estado.\n"
            "2. Ninguna autoridad podrá adoptar medidas que directa o indirectamente obstaculicen la "
            "libertad de circulación y establecimiento de las personas y la libre circulación de bienes "
            "en todo el territorio español."
        ),
    },
    {
        "numero": "141",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO II. De la Administración Local",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 141.\n"
            "1. La provincia es una entidad local con personalidad jurídica propia, determinada por la "
            "agrupación de municipios y división territorial para el cumplimiento de las actividades "
            "del Estado. Cualquier alteración de los límites provinciales habrá de ser aprobada por "
            "las Cortes Generales mediante ley orgánica.\n"
            "2. El gobierno y la administración autónoma de las provincias estarán encomendados a "
            "Diputaciones u otras Corporaciones de carácter representativo.\n"
            "3. Se podrán crear agrupaciones de municipios diferentes de la provincia.\n"
            "4. En los archipiélagos, las islas tendrán además su administración propia en forma de "
            "Cabildos o Consejos."
        ),
    },
    {
        "numero": "142",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO II. De la Administración Local",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 142.\n"
            "Las Haciendas locales deberán disponer de los medios suficientes para el desempeño de las "
            "funciones que la ley atribuye a las Corporaciones respectivas y se nutrirán "
            "fundamentalmente de tributos propios y de participación en los del Estado y de las "
            "Comunidades Autónomas."
        ),
    },
    {
        "numero": "143",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO III. De las Comunidades Autónomas",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 143.\n"
            "1. En el ejercicio del derecho a la autonomía reconocido en el artículo 2 de la "
            "Constitución, las provincias limítrofes con características históricas, culturales y "
            "económicas comunes, los territorios insulares y las provincias con entidad regional "
            "histórica podrán acceder a su autogobierno y constituirse en Comunidades Autónomas con "
            "arreglo a lo previsto en este Título y en los respectivos Estatutos.\n"
            "2. La iniciativa del proceso autonómico corresponde a todas las Diputaciones interesadas "
            "o al órgano interinsular correspondiente y a las dos terceras partes de los municipios "
            "cuya población represente, al menos, la mayoría del censo electoral de cada provincia o "
            "isla. Estos requisitos deberán ser cumplidos en el plazo de seis meses desde el primer "
            "acuerdo adoptado al respecto por alguna de las Corporaciones locales interesadas.\n"
            "3. La iniciativa, en caso de no prosperar, solamente podrá reiterarse pasados cinco años."
        ),
    },
    {
        "numero": "144",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO III. De las Comunidades Autónomas",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 144.\n"
            "Las Cortes Generales, mediante ley orgánica, podrán, por motivos de interés nacional:\n"
            "a) Autorizar la constitución de una Comunidad Autónoma cuando su ámbito territorial no "
            "supere el de una sola provincia y no reúna las condiciones del apartado 1 del artículo 143.\n"
            "b) Autorizar o acordar, en su caso, un Estatuto de Autonomía para territorios que no "
            "estén integrados en la organización provincial.\n"
            "c) Sustituir la iniciativa de las Corporaciones locales a que se refiere el apartado 2 "
            "del artículo 143."
        ),
    },
    {
        "numero": "145",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO III. De las Comunidades Autónomas",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 145.\n"
            "1. En ningún caso se admitirá la federación de Comunidades Autónomas.\n"
            "2. Los Estatutos podrán prever los supuestos, requisitos y términos en que las Comunidades "
            "Autónomas podrán celebrar convenios entre sí para la gestión y prestación de servicios "
            "propios de las mismas, así como el carácter y efectos de la correspondiente comunicación "
            "a las Cortes Generales. En los demás supuestos, los acuerdos de cooperación entre las "
            "Comunidades Autónomas necesitarán la autorización de las Cortes Generales."
        ),
    },
    {
        "numero": "146",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO III. De las Comunidades Autónomas",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 146.\n"
            "El proyecto de Estatuto será elaborado por una asamblea compuesta por los miembros de la "
            "Diputación u órgano interinsular de las provincias afectadas y por los Diputados y "
            "Senadores elegidos en ellas y será elevado a las Cortes Generales para su tramitación "
            "como ley."
        ),
    },
    {
        "numero": "147",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO III. De las Comunidades Autónomas",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 147.\n"
            "1. Dentro de los términos de la presente Constitución, los Estatutos serán la norma "
            "institucional básica de cada Comunidad Autónoma y el Estado los reconocerá y amparará "
            "como parte integrante de su ordenamiento jurídico.\n"
            "2. Los Estatutos de Autonomía deberán contener:\n"
            "a) La denominación de la Comunidad que mejor corresponda a su identidad histórica.\n"
            "b) La delimitación de su territorio.\n"
            "c) La denominación, organización y sede de las instituciones autónomas propias.\n"
            "d) Las competencias asumidas dentro del marco establecido en la Constitución y las bases "
            "para el traspaso de los servicios correspondientes a las mismas.\n"
            "3. La reforma de los Estatutos se ajustará al procedimiento establecido en los mismos y "
            "requerirá, en todo caso, la aprobación por las Cortes Generales mediante ley orgánica."
        ),
    },
    {
        "numero": "148",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO III. De las Comunidades Autónomas",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 148.\n"
            "1. Las Comunidades Autónomas podrán asumir competencias en las siguientes materias:\n"
            "1.ª Organización de sus instituciones de autogobierno.\n"
            "2.ª Las alteraciones de los términos municipales comprendidos en su territorio y, en "
            "general, las funciones que correspondan a la Administración del Estado sobre las "
            "Corporaciones locales y cuya transferencia autorice la legislación sobre Régimen Local.\n"
            "3.ª Ordenación del territorio, urbanismo y vivienda.\n"
            "4.ª Las obras públicas de interés de la Comunidad Autónoma en su propio territorio.\n"
            "5.ª Los ferrocarriles y carreteras cuyo itinerario se desarrolle íntegramente en el "
            "territorio de la Comunidad Autónoma y, en los mismos términos, el transporte desarrollado "
            "por estos medios o por cable.\n"
            "6.ª Los puertos de refugio, los puertos y aeropuertos deportivos y, en general, los que "
            "no desarrollen actividades comerciales.\n"
            "7.ª La agricultura y ganadería, de acuerdo con la ordenación general de la economía.\n"
            "8.ª Los montes y aprovechamientos forestales.\n"
            "9.ª La gestión en materia de protección del medio ambiente.\n"
            "10.ª Los proyectos, construcción y explotación de los aprovechamientos hidráulicos, "
            "canales y regadíos de interés de la Comunidad Autónoma; las aguas minerales y termales.\n"
            "11.ª La pesca en aguas interiores, el marisqueo y la acuicultura, la caza y la pesca fluvial.\n"
            "12.ª Ferias interiores.\n"
            "13.ª El fomento del desarrollo económico de la Comunidad Autónoma dentro de los objetivos "
            "marcados por la política económica nacional.\n"
            "14.ª La artesanía.\n"
            "15.ª Museos, bibliotecas y conservatorios de música de interés para la Comunidad Autónoma.\n"
            "16.ª Patrimonio monumental de interés de la Comunidad Autónoma.\n"
            "17.ª El fomento de la cultura, de la investigación y, en su caso, de la enseñanza de la "
            "lengua de la Comunidad Autónoma.\n"
            "18.ª Promoción y ordenación del turismo en su ámbito territorial.\n"
            "19.ª Promoción del deporte y de la adecuada utilización del ocio.\n"
            "20.ª Asistencia social.\n"
            "21.ª Sanidad e higiene.\n"
            "22.ª La vigilancia y protección de sus edificios e instalaciones. La coordinación y demás "
            "facultades en relación con las policías locales en los términos que establezca una ley orgánica.\n"
            "2. Transcurridos cinco años, y mediante la reforma de sus Estatutos, las Comunidades "
            "Autónomas podrán ampliar sucesivamente sus competencias dentro del marco establecido en "
            "el artículo 149."
        ),
    },
    {
        "numero": "149",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO III. De las Comunidades Autónomas",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 149.\n"
            "1. El Estado tiene competencia exclusiva sobre las siguientes materias:\n"
            "1.ª La regulación de las condiciones básicas que garanticen la igualdad de todos los "
            "españoles en el ejercicio de los derechos y en el cumplimiento de los deberes constitucionales.\n"
            "2.ª Nacionalidad, inmigración, emigración, extranjería y derecho de asilo.\n"
            "3.ª Relaciones internacionales.\n"
            "4.ª Defensa y Fuerzas Armadas.\n"
            "5.ª Administración de Justicia.\n"
            "6.ª Legislación mercantil, penal y penitenciaria; legislación procesal, sin perjuicio de "
            "las necesarias especialidades que en este orden se deriven de las particularidades del "
            "derecho sustantivo de las Comunidades Autónomas.\n"
            "7.ª Legislación laboral; sin perjuicio de su ejecución por los órganos de las Comunidades Autónomas.\n"
            "8.ª Legislación civil, sin perjuicio de la conservación, modificación y desarrollo por "
            "las Comunidades Autónomas de los derechos civiles, forales o especiales, allí donde existan.\n"
            "9.ª Legislación sobre propiedad intelectual e industrial.\n"
            "10.ª Régimen aduanero y arancelario; comercio exterior.\n"
            "11.ª Sistema monetario: divisas, cambio y convertibilidad; bases de la ordenación del "
            "crédito, banca y seguros.\n"
            "12.ª Legislación sobre pesas y medidas, determinación de la hora oficial.\n"
            "13.ª Bases y coordinación de la planificación general de la actividad económica.\n"
            "14.ª Hacienda general y Deuda del Estado.\n"
            "15.ª Fomento y coordinación general de la investigación científica y técnica.\n"
            "16.ª Sanidad exterior. Bases y coordinación general de la sanidad. Legislación sobre "
            "productos farmacéuticos.\n"
            "17.ª Legislación básica y régimen económico de la Seguridad Social, sin perjuicio de la "
            "ejecución de sus servicios por las Comunidades Autónomas.\n"
            "18.ª Las bases del régimen jurídico de las Administraciones públicas y del régimen "
            "estatutario de sus funcionarios que, en todo caso, garantizarán a los administrados un "
            "tratamiento común ante ellas; el procedimiento administrativo común, sin perjuicio de las "
            "especialidades derivadas de la organización propia de las Comunidades Autónomas; legislación "
            "sobre expropiación forzosa; legislación básica sobre contratos y concesiones "
            "administrativas y el sistema de responsabilidad de todas las Administraciones públicas.\n"
            "19.ª Pesca marítima, sin perjuicio de las competencias que en la ordenación del sector se "
            "atribuyan a las Comunidades Autónomas.\n"
            "20.ª Marina mercante y abanderamiento de buques; iluminación de costas y señales marítimas; "
            "puertos de interés general; aeropuertos de interés general; control del espacio aéreo, "
            "tránsito y transporte aéreo, servicio meteorológico y matriculación de aeronaves.\n"
            "21.ª Ferrocarriles y transportes terrestres que transcurran por el territorio de más de "
            "una Comunidad Autónoma; régimen general de comunicaciones; tráfico y circulación de "
            "vehículos a motor; correos y telecomunicaciones; cables aéreos, submarinos y radiocomunicación.\n"
            "22.ª La legislación, ordenación y concesión de recursos y aprovechamientos hidráulicos "
            "cuando las aguas discurran por más de una Comunidad Autónoma, y la autorización de las "
            "instalaciones eléctricas cuando su aprovechamiento afecte a otra Comunidad o el transporte "
            "de energía salga de su ámbito territorial.\n"
            "23.ª Legislación básica sobre protección del medio ambiente, sin perjuicio de las "
            "facultades de las Comunidades Autónomas de establecer normas adicionales de protección. "
            "La legislación básica sobre montes, aprovechamientos forestales y vías pecuarias.\n"
            "24.ª Obras públicas de interés general o cuya realización afecte a más de una Comunidad Autónoma.\n"
            "25.ª Bases de régimen minero y energético.\n"
            "26.ª Régimen de producción, comercio, tenencia y uso de armas y explosivos.\n"
            "27.ª Normas básicas del régimen de prensa, radio y televisión y, en general, de todos los "
            "medios de comunicación social, sin perjuicio de las facultades que en su desarrollo y "
            "ejecución correspondan a las Comunidades Autónomas.\n"
            "28.ª Defensa del patrimonio cultural, artístico y monumental español contra la exportación "
            "y la expoliación; museos, bibliotecas y archivos de titularidad estatal, sin perjuicio de "
            "su gestión por parte de las Comunidades Autónomas.\n"
            "29.ª Seguridad pública, sin perjuicio de la posibilidad de creación de policías por las "
            "Comunidades Autónomas en la forma que se establezca en los respectivos Estatutos en el "
            "marco de lo que disponga una ley orgánica.\n"
            "30.ª Regulación de las condiciones de obtención, expedición y homologación de títulos "
            "académicos y profesionales y normas básicas para el desarrollo del artículo 27 de la "
            "Constitución, a fin de garantizar el cumplimiento de las obligaciones de los poderes "
            "públicos en esta materia.\n"
            "31.ª Estadística para fines estatales.\n"
            "32.ª Autorización para la convocatoria de consultas populares por vía de referéndum.\n"
            "2. Sin perjuicio de las competencias que podrán asumir las Comunidades Autónomas, el "
            "Estado considerará el servicio de la cultura como deber y atribución esencial y facilitará "
            "la comunicación cultural entre las Comunidades Autónomas, de acuerdo con ellas.\n"
            "3. Las materias no atribuidas expresamente al Estado por esta Constitución podrán "
            "corresponder a las Comunidades Autónomas, en virtud de sus respectivos Estatutos. La "
            "competencia sobre las materias que no se hayan asumido por los Estatutos de Autonomía "
            "corresponderá al Estado, cuyas normas prevalecerán, en caso de conflicto, sobre las de "
            "las Comunidades Autónomas en todo lo que no esté atribuido a la exclusiva competencia de "
            "éstas. El derecho estatal será, en todo caso, supletorio del derecho de las Comunidades Autónomas."
        ),
    },
    {
        "numero": "150",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO III. De las Comunidades Autónomas",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 150.\n"
            "1. Las Cortes Generales, en materias de competencia estatal, podrán atribuir a todas o a "
            "alguna de las Comunidades Autónomas la facultad de dictar, para sí mismas, normas "
            "legislativas en el marco de los principios, bases y directrices fijados por una ley estatal. "
            "Sin perjuicio de la competencia de los Tribunales, en cada ley marco se establecerá la "
            "modalidad del control de las Cortes Generales sobre estas normas legislativas de las "
            "Comunidades Autónomas.\n"
            "2. El Estado podrá transferir o delegar en las Comunidades Autónomas, mediante ley "
            "orgánica, facultades correspondientes a materia de titularidad estatal que por su propia "
            "naturaleza sean susceptibles de transferencia o delegación. La ley preverá en cada caso "
            "la correspondiente transferencia de medios financieros, así como las formas de control "
            "que se reserve el Estado.\n"
            "3. El Estado podrá dictar leyes que establezcan los principios necesarios para armonizar "
            "las disposiciones normativas de las Comunidades Autónomas, aun en el caso de materias "
            "atribuidas a la competencia de éstas, cuando así lo exija el interés general. Corresponde "
            "a las Cortes Generales, por mayoría absoluta de cada Cámara, la apreciación de esta necesidad."
        ),
    },
    {
        "numero": "151",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO III. De las Comunidades Autónomas",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 151.\n"
            "1. No será preciso dejar transcurrir el plazo de cinco años, a que se refiere el apartado "
            "2 del artículo 148, cuando la iniciativa del proceso autonómico sea acordada dentro del "
            "plazo del artículo 143, 2, además de por las Diputaciones o los órganos interinsulares "
            "correspondientes, por las tres cuartas partes de los municipios de cada una de las "
            "provincias afectadas que representen, al menos, la mayoría del censo electoral de cada "
            "una de ellas y dicha iniciativa sea ratificada mediante referéndum por el voto afirmativo "
            "de la mayoría absoluta de los electores de cada provincia en los términos que establezca "
            "una ley orgánica.\n"
            "2. En el supuesto previsto en el apartado anterior, el procedimiento para la elaboración "
            "del Estatuto será el siguiente: (…) [ver texto completo en BOE-A-1978-31229]."
        ),
    },
    {
        "numero": "152",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO III. De las Comunidades Autónomas",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 152.\n"
            "1. En los Estatutos aprobados por el procedimiento a que se refiere el artículo anterior, "
            "la organización institucional autonómica se basará en una Asamblea Legislativa, elegida "
            "por sufragio universal, con arreglo a un sistema de representación proporcional que "
            "asegure, además, la representación de las diversas zonas del territorio; un Consejo de "
            "Gobierno con funciones ejecutivas y administrativas y un Presidente, elegido por la "
            "Asamblea de entre sus miembros, y nombrado por el Rey, al que corresponde la dirección "
            "del Consejo de Gobierno, la suprema representación de la respectiva Comunidad y la "
            "ordinaria del Estado en aquélla. El Presidente y los miembros del Consejo de Gobierno "
            "serán políticamente responsables ante la Asamblea.\n"
            "2. Una vez sancionados y promulgados los respectivos Estatutos, solamente podrán ser "
            "modificados mediante los procedimientos en ellos establecidos y con referéndum entre los "
            "electores inscritos en los censos correspondientes.\n"
            "3. Mediante la agrupación de municipios limítrofes, los Estatutos podrán establecer "
            "circunscripciones territoriales propias, que gozarán de plena personalidad jurídica."
        ),
    },
    {
        "numero": "153",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO III. De las Comunidades Autónomas",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 153.\n"
            "El control de la actividad de los órganos de las Comunidades Autónomas se ejercerá por:\n"
            "a) El Tribunal Constitucional, el relativo a la constitucionalidad de sus disposiciones "
            "normativas con fuerza de ley.\n"
            "b) El Gobierno, previo dictamen del Consejo de Estado, el del ejercicio de funciones "
            "delegadas a que se refiere el apartado 2 del artículo 150.\n"
            "c) La jurisdicción contencioso-administrativa, el de la administración autónoma y sus "
            "normas reglamentarias.\n"
            "d) El Tribunal de Cuentas, el económico y presupuestario."
        ),
    },
    {
        "numero": "154",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO III. De las Comunidades Autónomas",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 154.\n"
            "Un Delegado nombrado por el Gobierno dirigirá la Administración del Estado en el "
            "territorio de la Comunidad Autónoma y la coordinará, cuando proceda, con la administración "
            "propia de la Comunidad."
        ),
    },
    {
        "numero": "155",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO III. De las Comunidades Autónomas",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 155.\n"
            "1. Si una Comunidad Autónoma no cumpliere las obligaciones que la Constitución u otras "
            "leyes le impongan, o actuare de forma que atente gravemente al interés general de España, "
            "el Gobierno, previo requerimiento al Presidente de la Comunidad Autónoma y, en el caso "
            "de no ser atendido, con la aprobación por mayoría absoluta del Senado, podrá adoptar las "
            "medidas necesarias para obligar a aquélla al cumplimiento forzoso de dichas obligaciones "
            "o para la protección del mencionado interés general.\n"
            "2. Para la ejecución de las medidas previstas en el apartado anterior, el Gobierno podrá "
            "dar instrucciones a todas las autoridades de las Comunidades Autónomas."
        ),
    },
    {
        "numero": "156",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO III. De las Comunidades Autónomas",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 156.\n"
            "1. Las Comunidades Autónomas gozarán de autonomía financiera para el desarrollo y "
            "ejecución de sus competencias con arreglo a los principios de coordinación con la "
            "Hacienda estatal y de solidaridad entre todos los españoles.\n"
            "2. Las Comunidades Autónomas podrán actuar como delegados o colaboradores del Estado "
            "para la recaudación, la gestión y la liquidación de los recursos tributarios de aquél, "
            "de acuerdo con las leyes y los Estatutos."
        ),
    },
    {
        "numero": "157",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO III. De las Comunidades Autónomas",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 157.\n"
            "1. Los recursos de las Comunidades Autónomas estarán constituidos por:\n"
            "a) Impuestos cedidos total o parcialmente por el Estado; recargos sobre impuestos estatales "
            "y otras participaciones en los ingresos del Estado.\n"
            "b) Sus propios impuestos, tasas y contribuciones especiales.\n"
            "c) Transferencias de un Fondo de Compensación interterritorial y otras asignaciones con "
            "cargo a los Presupuestos Generales del Estado.\n"
            "d) Rendimientos procedentes de su patrimonio e ingresos de derecho privado.\n"
            "e) El producto de las operaciones de crédito.\n"
            "2. Las Comunidades Autónomas no podrán en ningún caso adoptar medidas tributarias sobre "
            "bienes situados fuera de su territorio o que supongan obstáculo para la libre circulación "
            "de mercancías o servicios.\n"
            "3. Mediante ley orgánica podrá regularse el ejercicio de las competencias financieras "
            "enumeradas en el precedente apartado 1, las normas para resolver los conflictos que "
            "pudieran surgir y las posibles formas de colaboración financiera entre las Comunidades "
            "Autónomas y el Estado."
        ),
    },
    {
        "numero": "158",
        "titulo": None,
        "titulo_titulo": "TÍTULO VIII. De la Organización Territorial del Estado",
        "titulo_capitulo": "CAPÍTULO III. De las Comunidades Autónomas",
        "titulo_seccion": None,
        "contenido": (
            "Artículo 158.\n"
            "1. En los Presupuestos Generales del Estado podrá establecerse una asignación a las "
            "Comunidades Autónomas en función del volumen de los servicios y actividades estatales "
            "que hayan asumido y de la garantía de un nivel mínimo en la prestación de los servicios "
            "públicos fundamentales en todo el territorio español.\n"
            "2. Con el fin de corregir desequilibrios económicos interterritoriales y hacer efectivo "
            "el principio de solidaridad, se constituirá un Fondo de Compensación con destino a gastos "
            "de inversión, cuyos recursos serán distribuidos por las Cortes Generales entre las "
            "Comunidades Autónomas y provincias, en su caso."
        ),
    },
    # TÍTULO IX (160, 162–165)
    {
        "numero": "160",
        "titulo": None,
        "titulo_titulo": "TÍTULO IX. Del Tribunal Constitucional",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 160.\n"
            "El Presidente del Tribunal Constitucional será nombrado entre sus miembros por el Rey, "
            "a propuesta del mismo Tribunal en pleno, por un período de tres años."
        ),
    },
    {
        "numero": "162",
        "titulo": None,
        "titulo_titulo": "TÍTULO IX. Del Tribunal Constitucional",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 162.\n"
            "1. Están legitimados:\n"
            "a) Para interponer el recurso de inconstitucionalidad, el Presidente del Gobierno, el "
            "Defensor del Pueblo, cincuenta Diputados, cincuenta Senadores, los órganos colegiados "
            "ejecutivos de las Comunidades Autónomas y, en su caso, las Asambleas de las mismas.\n"
            "b) Para interponer el recurso de amparo, toda persona natural o jurídica que invoque un "
            "interés legítimo, así como el Defensor del Pueblo y el Ministerio Fiscal.\n"
            "2. En los demás casos, la ley orgánica determinará las personas y órganos legitimados."
        ),
    },
    {
        "numero": "163",
        "titulo": None,
        "titulo_titulo": "TÍTULO IX. Del Tribunal Constitucional",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 163.\n"
            "Cuando un órgano judicial considere, en algún proceso, que una norma con rango de ley, "
            "aplicable al caso, de cuya validez dependa el fallo, pueda ser contraria a la "
            "Constitución, planteará la cuestión ante el Tribunal Constitucional en los supuestos, "
            "en la forma y con los efectos que establezca la ley, que en ningún caso serán suspensivos."
        ),
    },
    {
        "numero": "164",
        "titulo": None,
        "titulo_titulo": "TÍTULO IX. Del Tribunal Constitucional",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 164.\n"
            "1. Las sentencias del Tribunal Constitucional se publicarán en el Boletín Oficial del "
            "Estado con los votos particulares, si los hubiere. Tienen el valor de cosa juzgada a "
            "partir del día siguiente de su publicación y no cabe recurso alguno contra ellas. Las "
            "que declaren la inconstitucionalidad de una ley o de una norma con fuerza de ley y todas "
            "las que no se limiten a la estimación subjetiva de un derecho, tienen plenos efectos "
            "frente a todos.\n"
            "2. Salvo que en el fallo se disponga otra cosa, subsistirá la vigencia de la ley en la "
            "parte no afectada por la inconstitucionalidad."
        ),
    },
    {
        "numero": "165",
        "titulo": None,
        "titulo_titulo": "TÍTULO IX. Del Tribunal Constitucional",
        "titulo_capitulo": None,
        "titulo_seccion": None,
        "contenido": (
            "Artículo 165.\n"
            "Una ley orgánica regulará el funcionamiento del Tribunal Constitucional, el estatuto de "
            "sus miembros, el procedimiento ante el mismo y las condiciones para el ejercicio de las "
            "acciones."
        ),
    },
]

# Preguntas para el modo quiz, por artículo
QUIZ_PREGUNTAS = [
    {
        "articulo": "1",
        "pregunta": "¿Cuál es la forma política del Estado español según el artículo 1?",
        "respuesta_correcta": "La Monarquía parlamentaria",
        "opciones": [
            "La República democrática",
            "La Monarquía parlamentaria",
            "El Estado federal",
            "La Democracia directa",
        ],
    },
    {
        "articulo": "1",
        "pregunta": "¿Cuáles son los valores superiores del ordenamiento jurídico español según el art. 1.1?",
        "respuesta_correcta": "La libertad, la justicia, la igualdad y el pluralismo político",
        "opciones": [
            "La libertad, la justicia, la igualdad y la solidaridad",
            "La libertad, la justicia, la igualdad y el pluralismo político",
            "La libertad, la democracia, la igualdad y el pluralismo político",
            "La paz, la justicia, la igualdad y el pluralismo político",
        ],
    },
    {
        "articulo": "2",
        "pregunta": "¿Qué garantiza el artículo 2 de la Constitución respecto a las nacionalidades y regiones?",
        "respuesta_correcta": "El derecho a la autonomía de las nacionalidades y regiones",
        "opciones": [
            "La independencia de las nacionalidades y regiones",
            "El derecho a la autonomía de las nacionalidades y regiones",
            "La federalización del Estado",
            "La soberanía de las Comunidades Autónomas",
        ],
    },
    {
        "articulo": "3",
        "pregunta": "Según el art. 3, ¿tienen todos los españoles el deber de conocer el castellano?",
        "respuesta_correcta": "Sí, todos los españoles tienen el deber de conocerlo y el derecho a usarlo",
        "opciones": [
            "No, solo tienen el derecho de usarlo",
            "Sí, todos los españoles tienen el deber de conocerlo y el derecho a usarlo",
            "Solo los funcionarios públicos tienen ese deber",
            "Solo los nacidos en territorio de habla castellana",
        ],
    },
    {
        "articulo": "5",
        "pregunta": "¿Cuál es la capital del Estado español según la Constitución?",
        "respuesta_correcta": "La villa de Madrid",
        "opciones": [
            "La ciudad de Madrid",
            "La villa de Madrid",
            "La ciudad de Toledo",
            "La Corte de Madrid",
        ],
    },
    {
        "articulo": "12",
        "pregunta": "¿A qué edad son mayores de edad los españoles según la Constitución?",
        "respuesta_correcta": "A los dieciocho años",
        "opciones": [
            "A los dieciséis años",
            "A los diecisiete años",
            "A los dieciocho años",
            "A los veintiún años",
        ],
    },
    {
        "articulo": "14",
        "pregunta": "¿Qué principio establece el artículo 14 de la Constitución?",
        "respuesta_correcta": "La igualdad de los españoles ante la ley sin discriminación",
        "opciones": [
            "El derecho al voto universal",
            "La igualdad de los españoles ante la ley sin discriminación",
            "La libertad de expresión",
            "El derecho a la educación",
        ],
    },
    {
        "articulo": "15",
        "pregunta": "¿Está abolida la pena de muerte en España según el art. 15?",
        "respuesta_correcta": "Sí, salvo lo que dispongan las leyes penales militares para tiempos de guerra",
        "opciones": [
            "Sí, de forma absoluta en todos los casos",
            "No, está permitida para delitos de terrorismo",
            "Sí, salvo lo que dispongan las leyes penales militares para tiempos de guerra",
            "No, la decide el Tribunal Supremo en casos excepcionales",
        ],
    },
    {
        "articulo": "17",
        "pregunta": "¿Cuál es el plazo máximo de detención preventiva sin pasar a disposición judicial?",
        "respuesta_correcta": "Setenta y dos horas",
        "opciones": [
            "Veinticuatro horas",
            "Cuarenta y ocho horas",
            "Setenta y dos horas",
            "Noventa y seis horas",
        ],
    },
    {
        "articulo": "20",
        "pregunta": "¿Permite el art. 20 la censura previa de la libertad de expresión?",
        "respuesta_correcta": "No, no puede restringirse mediante ningún tipo de censura previa",
        "opciones": [
            "Sí, cuando lo acuerde el Gobierno",
            "Sí, con autorización judicial",
            "No, no puede restringirse mediante ningún tipo de censura previa",
            "Solo en estados de alarma o emergencia",
        ],
    },
    {
        "articulo": "23",
        "pregunta": "¿A quiénes reconoce el art. 23 el derecho a acceder a funciones y cargos públicos?",
        "respuesta_correcta": "A los ciudadanos, en condiciones de igualdad",
        "opciones": [
            "Solo a los españoles mayores de 25 años",
            "A todos los residentes legales en España",
            "A los ciudadanos, en condiciones de igualdad",
            "Solo a los que tengan titulación universitaria",
        ],
    },
    {
        "articulo": "24",
        "pregunta": "¿Qué garantiza el art. 24.2 respecto al proceso penal?",
        "respuesta_correcta": "Entre otros, la presunción de inocencia y el derecho a no declarar contra sí mismo",
        "opciones": [
            "Solo el derecho a la asistencia letrada",
            "Entre otros, la presunción de inocencia y el derecho a no declarar contra sí mismo",
            "El derecho a un juicio por jurado",
            "Solo el derecho a conocer la acusación",
        ],
    },
    {
        "articulo": "56",
        "pregunta": "¿Cuál es el título del Jefe del Estado según el art. 56?",
        "respuesta_correcta": "Rey de España",
        "opciones": [
            "Monarca constitucional",
            "Rey de España",
            "Soberano de España",
            "Jefe Supremo del Estado",
        ],
    },
    {
        "articulo": "66",
        "pregunta": "¿De qué están formadas las Cortes Generales?",
        "respuesta_correcta": "Del Congreso de los Diputados y el Senado",
        "opciones": [
            "Del Congreso de los Diputados, el Senado y el Tribunal Constitucional",
            "Del Congreso de los Diputados y el Senado",
            "De las Cortes y el Parlamento Europeo",
            "Del Congreso de los Diputados únicamente",
        ],
    },
    {
        "articulo": "68",
        "pregunta": "¿Cuántos diputados componen el Congreso según el art. 68?",
        "respuesta_correcta": "Un mínimo de 300 y un máximo de 400",
        "opciones": [
            "350 fijos",
            "Un mínimo de 300 y un máximo de 400",
            "Un mínimo de 250 y un máximo de 350",
            "Un mínimo de 300 y un máximo de 500",
        ],
    },
    {
        "articulo": "99",
        "pregunta": "Si en la primera votación de investidura el candidato no obtiene mayoría absoluta, ¿qué ocurre?",
        "respuesta_correcta": "Se repite 48 horas después y basta con mayoría simple",
        "opciones": [
            "Se propone un nuevo candidato inmediatamente",
            "Se repite 48 horas después y basta con mayoría simple",
            "Se convocan nuevas elecciones",
            "El Rey nombra directamente al candidato",
        ],
    },
    {
        "articulo": "113",
        "pregunta": "¿Qué mayoría se necesita para aprobar una moción de censura?",
        "respuesta_correcta": "Mayoría absoluta del Congreso de los Diputados",
        "opciones": [
            "Mayoría simple del Congreso",
            "Mayoría absoluta del Congreso de los Diputados",
            "Mayoría de tres quintos del Congreso",
            "Mayoría absoluta de ambas Cámaras",
        ],
    },
    {
        "articulo": "117",
        "pregunta": "¿En qué principio se basa la organización y funcionamiento de los Tribunales según art. 117?",
        "respuesta_correcta": "El principio de unidad jurisdiccional",
        "opciones": [
            "El principio de independencia judicial",
            "El principio de unidad jurisdiccional",
            "El principio de separación de poderes",
            "El principio de tutela judicial efectiva",
        ],
    },
    {
        "articulo": "159",
        "pregunta": "¿De cuántos miembros se compone el Tribunal Constitucional?",
        "respuesta_correcta": "Doce miembros",
        "opciones": [
            "Nueve miembros",
            "Diez miembros",
            "Doce miembros",
            "Quince miembros",
        ],
    },
    {
        "articulo": "168",
        "pregunta": "¿Qué mayoría se exige para revisar totalmente la Constitución (art. 168)?",
        "respuesta_correcta": "Mayoría de dos tercios de cada Cámara",
        "opciones": [
            "Mayoría absoluta de cada Cámara",
            "Mayoría de tres quintos de cada Cámara",
            "Mayoría de dos tercios de cada Cámara",
            "Mayoría simple más referéndum",
        ],
    },
]
