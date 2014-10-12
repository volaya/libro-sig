#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import os.path
import sys
import fnmatch
import glob
import traceback
import json

tableshtml={
"Tabla:Combinacion_capas_categoricas": r"<table border='1'><colgroup><col width='24%' /><col width='30%' /><col width='46%' /></colgroup><thead valign='bottom'><tr class='row-odd'><th class='head'>Tipo</th><th class='head'>Valor original</th><th class='head'>Valor reclasificado</th></tr></thead><tbody valign='top'><tr class='row-even'><td>Suelo A</td><td>1</td><td>1</td></tr><tr class='row-odd'><td>Suelo B</td><td>2</td><td>2</td></tr><tr class='row-even'><td>Suelo C</td><td>3</td><td>4</td></tr><tr class='row-odd'><td>Uso suelo A</td><td>1</td><td>8</td></tr><tr class='row-even'><td>Uso suelo B</td><td>2</td><td>16</td></tr><tr class='row-odd'><td>Uso suelo C</td><td>3</td><td>32</td></tr></tbody></table>",
"Tabla:Combinacion_capas_categoricas2": r"<table border='1'><colgroup><col width='36%' /><col width='27%' /><col width='36%' /></colgroup><thead valign='bottom'><tr class='row-odd'><th class='head'>Valor resultante</th><th class='head'>Tipo suelo</th><th class='head'>Tipo uso suelo</th></tr></thead><tbody valign='top'><tr class='row-even'><td>9</td><td>Suelo A (1)</td><td>Uso suelo A (8)</td></tr><tr class='row-odd'><td>10</td><td>Suelo B (2)</td><td>Uso suelo A (8)</td></tr><tr class='row-even'><td>12</td><td>Suelo C (4)</td><td>Uso suelo A (8)</td></tr><tr class='row-odd'><td>17</td><td>Suelo A (1)</td><td>Uso suelo B (16)</td></tr><tr class='row-even'><td>18</td><td>Suelo B (2)</td><td>Uso suelo B (16)</td></tr><tr class='row-odd'><td>19</td><td>Suelo C (4)</td><td>Uso suelo B (16)</td></tr><tr class='row-even'><td>33</td><td>Suelo A (1)</td><td>Uso suelo C (32)</td></tr><tr class='row-odd'><td>34</td><td>Suelo B (2)</td><td>Uso suelo C (32)</td></tr><tr class='row-even'><td>36</td><td>Suelo C (4)</td><td>Uso suelo C (32)</td></tr></tbody></table>",
"Tabla:Tablas_base_union": r'<table border="1" class="docutils"><colgroup><col width="32%" /><col width="68%" /></colgroup><thead valign="bottom"><tr class="row-odd"><th class="head"><tt><span class="pre">ID</span></tt></th><th class="head"><tt><span class="pre">TIPO_SUELO</span></tt></th></tr></thead><tbody valign="top"><tr class="row-even"><td>1</td><td>3</td></tr><tr class="row-odd"><td>2</td><td>1</td></tr><tr class="row-even"><td>3</td><td>3</td></tr><tr class="row-odd"><td>4</td><td>3</td></tr><tr class="row-even"><td>5</td><td>2</td></tr></tbody></table><table border="1" class="docutils"><colgroup><col width="34%" /><col width="39%" /><col width="27%" /></colgroup><thead valign="bottom"><tr class="row-odd"><th class="head"><tt><span class="pre">TIPO_SUELO</span></tt></th><th class="head"><tt><span class="pre">NOMBRE_SUELO</span></tt></th><th class="head"><tt><span class="pre">APTITUD</span></tt></th></tr></thead><tbody valign="top"><tr class="row-even"><td>1</td><td>Fluvisol</td><td>5</td></tr><tr class="row-odd"><td>2</td><td>Cambisol</td><td>7</td></tr><tr class="row-even"><td>3</td><td>Leptosol</td><td>4</td></tr></tbody></table>',
"Tabla:Resultado_union": r'<table border="1"><colgroup><col width="18%" /><col width="29%" /><col width="31%" /><col width="22%" /></colgroup><thead valign="bottom"><tr class="row-odd"><th class="head"><tt><span class="pre">ID</span></tt></th><th class="head"><tt><span class="pre">TIPO_SUELO</span></tt></th><th class="head"><tt><span class="pre">NOMBRE_SUELO</span></tt></th><th class="head"><tt><span class="pre">APTITUD</span></tt></th></tr></thead><tbody valign="top"><tr class="row-even"><td>1</td><td>3</td><td>Leptosol</td><td>4</td></tr><tr class="row-odd"><td>2</td><td>1</td><td>Fluvisol</td><td>5</td></tr><tr class="row-even"><td>3</td><td>3</td><td>Leptosol</td><td>4</td></tr><tr class="row-odd"><td>4</td><td>3</td><td>Leptosol</td><td>4</td></tr><tr class="row-even"><td>5</td><td>2</td><td>Cambisol</td><td>7</td></tr></tbody></table>',
"Tabla:Matriz_contingencias": r'<table border="1"><colgroup><col width="18%" /><col width="18%" /><col width="18%" /><col width="21%" /><col width="24%" /></colgroup><thead valign="bottom"><tr class="row-odd"><th class="head">Clase</th><th class="head">A</th><th class="head">B</th><th class="head">C</th><th class="head">D</th></tr></thead><tbody valign="top"><tr class="row-even"><td>A</td><td>20135</td><td>15</td><td>20</td><td>0</td></tr><tr class="row-odd"><td>B</td><td>22</td><td>18756</td><td>133</td><td>512</td></tr><tr class="row-even"><td>C</td><td>19</td><td>70</td><td>30452</td><td>345</td></tr><tr class="row-odd"><td>D</td><td>3</td><td>457</td><td>272</td><td>7018</td></tr></tbody></table>',
"Tabla:AHP": r'<table border="1"><colgroup><col width="27%" /><col width="73%" /></colgroup><thead valign="bottom"><tr class="row-odd"><th class="head">Valor</th><th class="head">Descripción</th></tr></thead><tbody valign="top"><tr class="row-even"><td>1</td><td>Misma importancia</td></tr><tr class="row-odd"><td>3</td><td>Predominancia moderada de un factor sobre otro</td></tr><tr class="row-even"><td>5</td><td>Predominancia fuerte</td></tr><tr class="row-odd"><td>7</td><td>Predominancia muy fuerte</td></tr><tr class="row-even"><td>9</td><td>Predominancia extrema</td></tr><tr class="row-odd"><td>2, 4, 6, 8</td><td>Valores intermedios</td></tr><tr class="row-even"><td>Valores recíprocos</td><td>Valores para comparación inversa</td></tr></tbody></table>',
"Tabla:Vecino_mas_cercano": r'<table border="1"><colgroup><col width="30%" /><col width="35%" /><col width="15%" /><col width="20%" /></colgroup><thead valign="bottom"><tr class="row-odd"><th class="head">Parámetro</th><th class="head">Aleatoria</th><th class="head">Regular</th><th class="head">Agregada</th></tr></thead><tbody valign="top"><tr class="row-even"><td>Dist. media</td><td>8,802</td><td>13,658</td><td>3,759</td></tr><tr class="row-odd"><td>Varianza</td><td>0,599</td><td>0,654</td><td>0,419</td></tr><tr class="row-even"><td>Varianza corr.</td><td>0,659</td><td>1,03</td><td>0,942</td></tr><tr class="row-odd"><td>NNI</td><td>1,487</td><td>2,207</td><td>0,759</td></tr><tr class="row-even"><td>NNI corr.</td><td>1,323</td><td>1,964</td><td>0,675</td></tr></tbody></table>',
"Tabla:Visibilidad": r'<table border="1"><colgroup><col width="14%" /><col width="12%" /><col width="22%" /><col width="32%" /><col width="21%" /></colgroup><thead valign="bottom"><tr class="row-odd"><th class="head">Fila, col.</th><th class="head"><span class="math">\(H\)</span></th><th class="head"><span class="math">\(\Delta H\)</span></th><th class="head"><span class="math">\(\Delta H/ Dist.\)</span></th><th class="head">Visible sí/no</th></tr></thead><tbody valign="top"><tr class="row-even"><td>1,2</td><td>14</td><td>4</td><td>4</td><td>Visible</td></tr><tr class="row-odd"><td>1,3</td><td>19</td><td>9</td><td>4.5</td><td>Visible</td></tr><tr class="row-even"><td>1,4</td><td>22</td><td>12</td><td>4</td><td>No visible</td></tr><tr class="row-odd"><td>1,5</td><td>24</td><td>14</td><td>3.5</td><td>No visible</td></tr><tr class="row-even"><td>1,6</td><td>23</td><td>13</td><td>2.6</td><td>No visible</td></tr></tbody></table>',
"Tabla:Clasificacion_curvaturas":r'<table border="1"><colgroup><col width="23%" /><col width="38%" /><col width="39%" /></colgroup><thead valign="bottom"><tr class="row-odd"><th class="head">Tipo</th><th class="head"><span class="math">\(\frac{\partial^2 z}{\partial x}\)</span></th><th class="head"><span class="math">\(\frac{\partial^2 z}{\partial y}\)</span></th></tr></thead><tbody valign="top"><tr class="row-even"><td>Cima</td><td><span class="math">\(+\)</span></td><td><span class="math">\(+\)</span></td></tr><tr class="row-odd"><td>Collado(Punto de silla)</td><td><span class="math">\(+\)</span></td><td><span class="math">\(-\)</span></td></tr><tr class="row-even"><td>Cresta</td><td><span class="math">\(+\)</span></td><td>0</td></tr><tr class="row-odd"><td>Plano</td><td>0</td><td>0</td></tr><tr class="row-even"><td>Cauce</td><td><span class="math">\(-\)</span></td><td>0</td></tr><tr class="row-odd"><td>Depresión</td><td><span class="math">\(-\)</span></td><td><span class="math">\(-\)</span></td></tr></tbody></table>',
"Tabla:Relacion_onda_parametro": r'<table border="1"><colgroup><col width="24%" /><col width="40%" /><col width="36%" /></colgroup><thead valign="bottom"><tr class="row-odd"><th class="head">Región del espectro</th><th class="head">Procesos</th><th class="head">Aplicaciones</th></tr></thead><tbody valign="top"><tr class="row-even"><td>Rayos X</td><td>Procesos atómicos</td><td>Detección de elementos radiactivos</td></tr><tr class="row-odd"><td>Ultravioleta</td><td>Procesos electrónicos</td><td>Presencia de H y He en la atmósfera</td></tr><tr class="row-even"><td>Visible e IR cercano</td><td>Vibración molecular</td><td>Composición química de la superficiePropiedades biológicas</td></tr><tr class="row-odd"><td>IR medio</td><td>Vibración y rotación molecular</td><td>Composición química de la superficiey la atmósfera</td></tr><tr class="row-even"><td>IR térmico</td><td>Emisión térmica</td><td>Temperatura de la superficie y la atmósfera</td></tr><tr class="row-odd"><td>Microondas</td><td>Rotación molecular y emisión térmica</td><td>Composición química de la atmósfera. Propiedades físicas de la superficie.</td></tr></tbody></table>',
"Tabla:TerminologiaModeloRelacional": r'<table border="1"><colgroup><col width="52%" /><col width="48%" /></colgroup><thead valign="bottom"><tr class="row-odd"><th class="head">Terminología habitual</th><th class="head">Modelo relacional</th></tr></thead><tbody valign="top"><tr class="row-even"><td>Tabla</td><td>Relación</td></tr><tr class="row-odd"><td>Fila</td><td>Tupla</td></tr><tr class="row-even"><td>Columna</td><td>Atributo</td></tr><tr class="row-odd"><td>Número de filas</td><td>Cardinalidad</td></tr><tr class="row-even"><td>Valores posibles</td><td>Dominio</td></tr></tbody></table>',
"Tabla:clavePrimaria": r'<p><strong>Tabla a</strong></p><table border="1"><colgroup><col width="15%" /><col width="29%" /><col width="19%" /><col width="15%" /><col width="21%" /></colgroup><thead valign="bottom"><tr class="row-odd"><th class="head"><tt><span class="pre">DNI</span></tt></th><th class="head"><tt><span class="pre">Nombre</span></tt></th><th class="head"><tt><span class="pre">Altura</span></tt></th><th class="head"><tt><span class="pre">Edad</span></tt></th><th class="head"><tt><span class="pre">Ciudad</span></tt></th></tr></thead><tbody valign="top"><tr class="row-even"><td>50234561</td><td>Juan Gómez</td><td>1,85</td><td>35</td><td>Madrid</td></tr><tr class="row-odd"><td>13254673</td><td>Edurne Montero</td><td>1,60</td><td>30</td><td>Toledo</td></tr><tr class="row-even"><td>46576290</td><td>Luis Urrutia</td><td>1,75</td><td>46</td><td>Madrid</td></tr><tr class="row-odd"><td>38941882</td><td>Juan Gómez</td><td>1, 71</td><td>55</td><td>Valencia</td></tr></tbody></table><p><strong>Tabla b</strong></p><table border="1"><colgroup><col width="14%" /><col width="29%" /><col width="20%" /><col width="16%" /><col width="22%" /></colgroup><thead valign="bottom"><tr class="row-odd"><th class="head"><tt><span class="pre">ID</span></tt></th><th class="head"><tt><span class="pre">Nombre</span></tt></th><th class="head"><tt><span class="pre">Altura</span></tt></th><th class="head"><tt><span class="pre">Edad</span></tt></th><th class="head"><tt><span class="pre">Ciudad</span></tt></th></tr></thead><tbody valign="top"><tr class="row-even"><td>001</td><td>Juan Gómez</td><td>1,85</td><td>35</td><td>Madrid</td></tr><tr class="row-odd"><td>002</td><td>Edurne Montero</td><td>1,60</td><td>30</td><td>Toledo</td></tr><tr class="row-even"><td>003</td><td>Luis Urrutia</td><td>1,75</td><td>46</td><td>Madrid</td></tr><tr class="row-odd"><td>004</td><td>Juan Gómez</td><td>1, 71</td><td>55</td><td>Valencia</td></tr></tbody></table>',
"Tabla:TablaModeloRelacional2": r'<table border="1"><colgroup><col width="19%" /><col width="28%" /><col width="54%" /></colgroup><thead valign="bottom"><tr class="row-odd"><th class="head"><tt><span class="pre">Nombre</span></tt></th><th class="head"><tt><span class="pre">Habitantes</span></tt></th><th class="head"><tt>Superficie(km^2)</tt></th></tr></thead><tbody valign="top"><tr class="row-even"><td>Madrid</td><td>6386932</td><td>607</td></tr><tr class="row-odd"><td>Valencia</td><td>1564145</td><td>134</td></tr><tr class="row-even"><td>Toledo</td><td>80810</td><td>232</td></tr></tbody></table>',
"Tabla:TablaConjunta": r'<table border="1"><colgroup><col width="10%" /><col width="17%" /><col width="13%" /><col width="11%" /><col width="13%" /><col width="17%" /><col width="18%" /></colgroup><thead valign="bottom"><tr class="row-odd"><th class="head"><tt><span class="pre">DNI</span></tt></th><th class="head"><tt><span class="pre">Nombre</span></tt></th><th class="head"><tt><span class="pre">Altura</span></tt></th><th class="head"><tt><span class="pre">Edad</span></tt></th><th class="head"><tt><span class="pre">Ciudad</span></tt></th><th class="head"><tt><span class="pre">Población</span></tt></th><th class="head"><tt><span class="pre">Superficie</span></tt></th></tr></thead><tbody valign="top"><tr class="row-even"><td>50234561</td><td>Juan Gómez</td><td>1,85</td><td>35</td><td>Madrid</td><td>6386932</td><td>607</td></tr><tr class="row-odd"><td>13254673</td><td>Edurne Montero</td><td>1,60</td><td>30</td><td>Toledo</td><td>80810</td><td>232</td></tr><tr class="row-even"><td>46576290</td><td>Luis Urrutia</td><td>1,75</td><td>46</td><td>Madrid</td><td>6386932</td><td>607</td></tr><tr class="row-odd"><td>38941882</td><td>Juan Gomez</td><td>1, 71</td><td>55</td><td>Valencia</td><td>1564145</td><td>134</td></tr></tbody></table>',
"Tabla:INSPIREAnexos": r'<ul><li><p class="first">Anexo I. Datos de referencia</p><blockquote><div><ul class="simple"><li>Sistema de ref. de coordenadas</li><li>Cuadrículas geográficas</li><li>Nombres geográficos</li><li>Unidades administrativas</li><li>Redes de transporte</li><li>Hidrografía</li><li>Lugares protegidos</li></ul></div></blockquote></li><li><p class="first">Anexo II</p><blockquote><div><ul class="simple"><li>Modelos de Elevaciones</li><li>Direcciones y áreas postales</li><li>Parcelas catastrales</li><li>Ocupación del suelo</li><li>Ortofotos</li></ul></div></blockquote></li><li><p class="first">Anexo III. Datos temáticos</p><blockquote><div><ul class="simple"><li>Unidades estadísticas</li><li>Edificaciones</li><li>Edafología</li><li>Geología</li><li>Uso del suelo</li><li>Salud y seguridad humana</li><li>Instalaciones de servicios</li><li>Instalaciones industriales y productivas</li><li>Instalaciones Agrícolas y Acuicultura</li><li>Hábitats y biotopos</li><li>Regiones biogeográficas</li><li>Demografía y distribución de la población</li><li>Áreas restringidas o reguladas</li><li>Zonas de riesgos naturales</li><li>Condiciones Atmosféricas</li><li>Características meteorológicas</li><li>Características oceanográficas</li><li>Regiones Marinas</li></ul>',
"Tabla:LaboresUsuariosSIG": r'<table border="1"><colgroup><col width="24%" /><col width="38%" /><col width="38%" /></colgroup><thead valign="bottom"><tr class="row-odd"><th class="head">Actor</th><th class="head">Tareas</th><th class="head">Actores específicos</th></tr></thead><tbody valign="top"><tr class="row-even"><td>Proveedores de datos</td><td>Generan nuevos datos espaciales.Son los dueños de los datos del sistema.Proveen información espacial.</td><td>Grupos de investigación dentro de la institución.Otras entidades interesadas en el mismo espacio.</td></tr><tr class="row-odd"><td>Administradores de datos</td><td>Mantenimiento y estandarización de datos espaciales.Mantenimiento de los procesos que aseguran eficienciay estandarización para manejar y entregar datos.</td><td>Especialistas en SIG y programación.</td></tr><tr class="row-even"><td>Usuarios de datos</td><td>Acceso y recombinación de datos espaciales.Generación de nueva información geográfica.y de bases de datos.Adición de conocimientos, hechos, interpretacionesy análisis al sistema.</td><td>Profesionales en GIS y geografía.Analistas de información espacial.Planificadores</td></tr><tr class="row-odd"><td>Clientes y usuarios de datos</td><td>Uso de la información y de los datos geográficos</td><td>De diversa naturaleza, interesados en los fenómenos</td></tr><tr class="row-even"><td>fuera de la institución.</td><td>generados a partir del SIG institucional.</td><td>espaciales.</td></tr></tbody></table>',
"Tabla:Elipsoides": r'<table border="1"><colgroup><col width="42%" /><col width="17%" /><col width="17%" /><col width="24%" /></colgroup><thead valign="bottom"><tr class="row-odd"><th class="head">Elipsoide</th><th class="head">Semieje mayor</th><th class="head">Semieje menor</th><th class="head"><span class="math">\(\frac{1}{f}\)</span></th></tr></thead><tbody valign="top"><tr class="row-even"><td>Australian National</td><td>6378160.000</td><td>6356774.719</td><td>298.250000</td></tr><tr class="row-odd"><td>Bessel 1841</td><td>6377397.155</td><td>6356078.963</td><td>299.152813</td></tr><tr class="row-even"><td>Clarke 1866</td><td>6378206.400</td><td>6356583.800</td><td>294.978698</td></tr><tr class="row-odd"><td>Clarke 1880</td><td>6378249.145</td><td>6356514.870</td><td>293.465000</td></tr><tr class="row-even"><td>Everest 1956</td><td>6377301.243</td><td>6356100.228</td><td>300.801700</td></tr><tr class="row-odd"><td>Fischer 1968</td><td>6378150.000</td><td>6356768.337</td><td>298.300000</td></tr><tr class="row-even"><td>GRS 1980</td><td>6378137.000</td><td>6356752.314</td><td>298.257222</td></tr><tr class="row-odd"><td>International 1924 (Hayford)</td><td>6378388.000</td><td>6356911.946</td><td>297.000000</td></tr><tr class="row-even"><td>SGS 85</td><td>6378136.000</td><td>6356751.302</td><td>298.257000</td></tr><tr class="row-odd"><td>South American 1969</td><td>6378160.000</td><td>6356774.719</td><td>298.250000</td></tr><tr class="row-even"><td>WGS 72</td><td>6378135.000</td><td>6356750.520</td><td>298.260000</td></tr><tr class="row-odd"><td>WGS 84</td><td>6378137.000</td><td>6356752.314</td><td>298.257224</td></tr></tbody></table>',
"Tabla:Coordenadas_ciudades": r'<table border="1"><colgroup><col width="33%" /><col width="33%" /><col width="33%" /></colgroup><thead valign="bottom"><tr class="row-odd"><th class="head">Ciudad</th><th class="head">Latitud</th><th class="head">Longitud</th></tr></thead><tbody valign="top"><tr class="row-even"><td>Badajoz</td><td>38.53 N</td><td>6.58 O</td></tr><tr class="row-odd"><td>Barcelona</td><td>41.23 N</td><td>2.11 E</td></tr><tr class="row-even"><td>Cadiz</td><td>36.32 N</td><td>6.18 O</td></tr><tr class="row-odd"><td>Girona</td><td>41.59 N</td><td>2.49 E</td></tr><tr class="row-even"><td>Granada</td><td>37.11 N</td><td>3.35 O</td></tr><tr class="row-odd"><td>Madrid</td><td>40.24 N</td><td>3.41 O</td></tr><tr class="row-even"><td>Segovia</td><td>40.57 N</td><td>4.07 O</td></tr><tr class="row-odd"><td>Valencia</td><td>39.28 N</td><td>0.22 O</td></tr><tr class="row-even"><td>Zaragoza</td><td>41.39 N</td><td>0.52 O</td></tr></tbody></table>',
"Tabla:PropiedadesVariablesVisuales": r'<table border="1"><col width="11%" /><col width="13%" /><col width="13%" /><col width="13%" /><col width="13%" /><col width="13%" /><col width="13%" /><col width="13%" /></colgroup><thead valign="bottom"><tr class="row-odd"><th class="head">Propiedad</th><th class="head">Posición</th><th class="head">Tamaño</th><th class="head">Forma</th><th class="head">Valor</th><th class="head">Tono</th><th class="head">Textura</th><th class="head">Orientación</th></tr></thead><tbody valign="top"><tr class="row-even"><td>Asociativa</td><td><span class="math">\(\diamondsuit\)</span></td><td>&#8212;</td><td><span class="math">\(\diamondsuit\)</span></td><td>&#8212;</td><td><span class="math">\(\diamondsuit\)</span></td><td><span class="math">\(\diamondsuit\)</span></td><td><span class="math">\(\diamondsuit\)</span></td></tr><tr class="row-odd"><td>Selectiva</td><td><span class="math">\(\diamondsuit\)</span></td><td><span class="math">\(\diamondsuit\)</span></td><td>&#8212;</td><td><span class="math">\(\diamondsuit\)</span></td><td><span class="math">\(\diamondsuit\)</span></td><td><span class="math">\(\diamondsuit\)</span></td><td><span class="math">\(\diamondsuit\)</span></td></tr><tr class="row-even"><td>Ordenada</td><td><span class="math">\(\diamondsuit\)</span></td><td><span class="math">\(\diamondsuit\)</span></td><td>&#8212;</td><td><span class="math">\(\diamondsuit\)</span></td><td>&#8212;</td><td>&#8212;</td><td>&#8212;</td></tr><tr class="row-odd"><td>Cuantitativa</td><td><span class="math">\(\diamondsuit\)</span></td><td><span class="math">\(\diamondsuit\)</span></td><td>&#8212;</td><td>&#8212;</td><td>&#8212;</td><td>&#8212;</td><td>&#8212;</td></tr></tbody></table>'
}

exps_pre = [(r"\\bigskip", ""),
        (r"\\ldots", "&hellip;"),  
        #(r"[\r\n]{2,}",r"<br><br>"),
        (r"\\centering", ""),
        (r"\\par[^t]", ""),
        (r"\\degree", "&deg;"),
        (r"\\noindent", ""),
        (r"\\vspace\{.*?\}", ""),
        (r"\\begin\{center\}", ""),
        (r"\\end\{center\}", ""),
        (r"\\small", "")]
        
exps_post = [(r"\\index\{.*?\}", ""),
        (r"\\pagestyle\{.*?\}",r""),
        (r"\\%", "%"),
        (r"\\_", "_"),
        (r"\\emph\{(.*?)\}", r"<i>\1</i>"),
        (r"\\underline\{(.*?)\}", r"<u>\1</u>"),
        (r"\\begin\{intro\}([\s\S]*?)\\end\{intro\}", 
            r'<hr/><p><i>\1</i></p><hr/>'), 
        (r"\url\{(.*?)}", r'<a href="\1">\1</a>'),
        (r"\\begin\{verbatim\}([\s\S]*?)\\end\{verbatim\}", r"<pre>\1</pre>"), 
        (r"\\begin\{quotation\}([\s\S]*?)\\end\{quotation\}", r"<p>\1</p>"), 
        (r"\\begin\{displaymath\}([\s\S]*?)\\end\{displaymath\}", r"\\begin{eqnarray}\1\\end{eqnarray}"), 
        (r"\\footnote\{[\s\S]*?\}", ""),
        (r"\\begin\{itemize\}", "<ul>"),
        (r"\\end\{itemize\}", "</ul>"),
        (r"\\begin\{enumerate\}", "<ol>"),
        (r"\\end\{enumerate\}", "</ol>"),
        (r"\\item", "<li>"),
        (r"\\subitem", ""),
        (r"\\texttt\{(.*?)\}", r"<tt>\1</tt>"),        
        (r"\\chapter.*?\{(.*?)\}", ""),
        (r"\\section.*?\{(.*?)\}", r'<h2 id="\1">\1</h2>'),
        (r"\\subsection.*?\{(.*?)\}", r'<h3 id="\1">\1</h3>'),
        (r"\\subsubsection.*?\{(.*?)\}", r'<h4 id="\1">\1</h4>'),
        (r"\\begin\{figure\}.*?\n", "<figure>"),
        (r"\\end\{figure\}", "</figure>"),
        (r"\\caption\{(.*)\}", r"<figcaption>\1</figcaption>"),
        (r"(\\label\{Fig:.*?\})", r"$$\1$$"),
        (r"---", "&#8212;"),
        (">>", "&raquo;"),
        ("<<", "&laquo;"),
        (r"([\s\S]*?)[\r\n]{2,}", r"<p>\1</p>"),  
        (r"<p><h",r"<h"),
        (r"(</h.>)</p>",r"\1"),
        (r"<p><pre>", r"<pre>"),
        (r"</pre></p>", r"</pre>"),
        (r"><br><br>",r"><br>"),
        ]


def template():
    path = "template.html"
    with open(path) as f:
        s = f.read()
    return s

labelrefs = {}

def convertFile(path):     
    name = os.path.splitext(os.path.basename(path))[0]
    with open(path) as f:
        s = f.read()

    for exp, replace in exps_pre:
        p = re.compile(exp)
        s = p.sub(replace, s) 

    p = re.compile(r"\\chapter.*?\{(.*?)\}")
    title = p.findall(s)[0]
    p = re.compile(r"\\chapterauthor\{(.*?)\}")
    authors = p.findall(s)
    p = re.compile(r"\\cite\{([ \S]*?)\}")
    cites = p.findall(s) 
    for cite in cites:
        rep = "".join(['[<a href="../bib.htm#%s">%s</a>]' % (c.strip(),c.strip()) for c in cite.split(",")])
        s = s.replace(r"\cite{%s}" % cite, rep)
    p = re.compile(r"(\\includegraphics.*?\{.*?\})")
    imgs = p.findall(s)
    for img in imgs:
        f = img[img.find("{")+1:img.rfind("}")]
        path, ext = os.path.splitext(f)
        if ext == ".pdf":
            ext = ".png"
        path = os.path.basename(path)
        size = img[img.find("["):img.rfind("]")]
        size = "".join([d for d in size if d in "0123456789."])
        try:
            size = float(size) * 100
        except:
            size = 100
        s = s.replace(img, r"<img src='../img/%s%s' width='%s'>" % (path, ext, str(size) + "%"))
    p = re.compile(r"\\label\{([^:]*?)\}")
    labels = p.findall(s)
    global labelrefs
    for label in labels:
        labelrefs[label] = name
    s = p.sub(r'<a name="\1"></a>', s) 

    p = re.compile(r"(\\begin\{table[\S\s]*?\\end\{table.*?\})")
    tables = p.findall(s)
    for table in tables:            
        idx = table.find("Tabla:")
        tablelabel = table[idx:table.find("}", idx)]
        idx = table.find(r"\caption") + 9        
        caption = table[idx:table.find("}\n", idx)]
        try:
            replace = tableshtml[tablelabel] + "<figcaption>%s</figcaption>$$\label{%s}$$" % (caption, tablelabel)
            s = s.replace(table, replace)            
        except Exception, e:
            print e
            pass

    for exp, replace in exps_post:
        p = re.compile(exp)
        s = p.sub(replace, s)            

    s = template().replace("[BODY]", s).replace("[TITLE]", title)
    if authors:
        s = s.replace("[AUTHOR]", "<p><i>%s</i></p>" % authors[0])
    else:
        s = s.replace("[AUTHOR]", "")
    with open(os.path.join("html/chapters", name + ".html"), "w") as f:
        f.write(s)



def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename
                
    
def convertImages():
    for f in find_files('../latex', '*.pdf'):

        from subprocess import call
        dest = os.path.basename(f)
        dest = os.path.splitext(dest)[0]
        dest = "img/%s.png" % dest
        commands = [r'"Inkscape.exe"', "--export-png=" + dest, f]
        print " ".join(commands)
        #call(commands)

if __name__ == '__main__':
    i = 0
    for f in find_files('../latex', '*.tex'):
        try:
            convertFile(f)
        except Exception, e:
            #traceback.print_exc()
            pass 
    for path in  glob.glob("html/chapters/*.html"):
        with open(path) as f:
            s = f.read()
        p = re.compile(r"\\ref\{([^:]*?)\}")
        refs = p.findall(s)
        for ref in refs:
            try:
                s = s.replace(r"\ref{%s}" % ref, '<a href="%s.html#%s">%s</a>' % (labelrefs[ref], ref, ref))
            except KeyError:
                pass
                #print ref
        with open(path, "w") as f:
            f.write(s)
