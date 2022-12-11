# TODO
# check semester also for qualitative grades



# main.py
from flask import Flask
import asyncio
from vx_api import get_vx_api_token
from vx_api import vx_api_get
from extension_api import get_all_proficiencies
from extension_api import get_all_outcomes_links
from extension_api import get_all_subjects
from extension_api import get_proficiency_values
from extension_api import get_all_letter_grades
from extension_api import get_letter_grade_values
from vx_tasks.get_classes import get_classes
from vx_tasks.get_qualitative_grades import get_qualitative_grades
from vx_tasks.get_letter_grades import get_letter_grades
from vx_tasks.get_grading_periods import get_grading_periods
from canvas_tasks.get_students import get_all_students
from canvas_tasks.get_outcomes import get_outcomes
from app import app
from datetime import datetime
import time


##################################################### 
# 
# Outcomes Veracross Data * temporary *
#
##################################################### 

vx_outcomes_data = [
    {'id': 8627, 'description': "Aesthetics: Apply aesthetic knowledge to create visual aids, documents, and decks"},
    {'id': 8628, 'description': "Design: Create a design brief that defines background, goals, timeline, constraints, and deliverables"},
    {'id': 8632, 'description': "Reading: Summarize the main ideas in college-level texts from a variety of disciplines"},
    {'id': 8634, 'description': "Life: Explain how simple biological systems interact, creating complex living systems"},
    {'id': 8646, 'description': "Critical Thinking: Analyze the sufficiency of the evidence in support of a claim"},
    {'id': 8650, 'description': "Research: Leverage search engines, databases, libraries, and archives independently and as appropriate to access information that answers a wide range of given and self-identified questions"},
    {'id': 8652, 'description': "Empathy: Take the perspectives of individuals, groups, and cultures into account and describe their points of view"},
    {'id': 8660, 'description': "Public Speaking: Design and deliver clear and compelling presentations that resonate with their intended audiences"},
    {'id': 8666, 'description': "Sustainability: Apply key principles of sustainability including scarcity, reduction, reuse, recycle, efficiency, life cycle, opportunity cost, and externalized costs to solve problems"},
    {'id': 8670, 'description': "Metacognition: Critique one's own performance and work, identifying strengths and weaknesses"},
    {'id': 8692, 'description': "Meaning: Analyze how individuals and communities have derived meaning and significance from art, literature, music, and philosophy"},
    {'id': 8693, 'description': "Design: Conduct user research to identify and explain needs and problems"},
    {'id': 8697, 'description': "Writing: Use syntactic structures, literary devices, and a range of vocabulary to deepen meaning and engage an intended audience with fluency"},
    {'id': 8699, 'description': "Evolution: Explain how complex life can naturally evolve from simple life"},
    {'id': 8711, 'description': "Reasoning: Analyze arguments presented in different forms including essays, speeches, editorials, graphs, and proofs"},
    {'id': 8715, 'description': "Writing: Proofread the structure and grammar of one's own and others' writing"},
    {'id': 8717, 'description': "Creativity: Seek out new and diverse perspectives on a given problem"},
    {'id': 8726, 'description': "Research: Organize and synthesize ideas, information, and quotations from multiple sources to inform a research question or project independently"},
    {'id': 8732, 'description': "Entrepreneurship: Identify novel examples of unmet needs and market opportunities"},
    {'id': 8735, 'description': "Planning: Design a plan independently by starting with the end goal and delineating the steps that will lead up to it"},
    {'id': 8757, 'description': "Creativity: Consider input and constructive feedback when creating or refining work"},
    {'id': 8758, 'description': "Design: Utilize techniques including empathy interviews, ideation and brainstorming, prototyping, testing solutions, and iterating"},
    {'id': 8762, 'description': "Public Speaking: Design and deliver clear and compelling presentations that resonate with their intended audiences"},
    {'id': 8764, 'description': "Ecosystems: Analyze the dynamics of a given ecosystem, explaining the complex web of dependencies between organisms and their environment"},
    {'id': 8777, 'description': "Discussion: Synthesize multiple perspectives and discussion points in one's own words"},
    {'id': 8781, 'description': "Critical Thinking: Acknowledge, respond to, and refute bias in both claims and evidence"},
    {'id': 8783, 'description': "Metacognition: Critique one's own performance and work, identifying strengths and weaknesses"},
    {'id': 8791, 'description': "Economics: Use economic tools and concepts to address public policy issues including competition, environmental protection, financial regulation, innovation and intellectual property, labor law, and taxation"},
    {'id': 8796, 'description': "Entrepreneurship: Employ business models, minimum viable product design, pro-forma statements, and cash flow projections to plan a venture"},
    {'id': 8799, 'description': "Creativity: Consider input and constructive feedback when creating or refining work"},
    {'id': 8821, 'description': "Classic Works: Situate a given work of art within its social, cultural, political, and historical context"},
    {'id': 8822, 'description': "Design: Develop prototypes to test, filter, and iterate ideas"},
    {'id': 8826, 'description': "Design: Create a design brief that defines background, goals, timeline, constraints, and deliverables"},
    {'id': 8828, 'description': "Scientific Method: Collect, represent, evaluate, and analyze experimental data to draw evidence-based conclusions"},
    {'id': 8840, 'description': "Research: Organize and synthesize ideas, information, and quotations from multiple sources to inform a research question or project independently"},
    {'id': 8843, 'description': "Reasoning: Craft an argument that supports a claim using clear reasoning and sound evidence"},
    {'id': 8845, 'description': "Mental Agility: Maintain focus and concentration on a given task for a designated period of time"},
    {'id': 8853, 'description': "System Dynamics: Predict how a given change will either damage or benefit a system as a whole"},
    {'id': 8859, 'description': "Reading: Summarize the main ideas in college-level texts from a variety of disciplines"},
    {'id': 8862, 'description': "Identity: Identify one's personal growth goals and areas of passion including how they contribute to a healthy sense of self"},
    {'id': 8881, 'description': "Planing: Design a plan independently by starting with the end goal and delineating the steps that will lead up to it"},
    {'id': 8882, 'description': "Design: Use digital technologies, fabrication, and processing tools to design and produce an artifact"},
    {'id': 8886, 'description': "Design: Develop prototypes to test, filter, and iterate ideas"},
    {'id': 8887, 'description': "Research: Organize and synthesize ideas, information, and quotations from multiple sources to inform a research question or project independently"},
    {'id': 8899, 'description': "Classic Works: Demonstrate familiarity with classic works of literature, art, and music both nationally and internationally"},
    {'id': 8902, 'description': "Trustworthiness: Commit to goals and see them through to accomplishment"},
    {'id': 8910, 'description': "Data Analysis: Record and interpret data that is presented in graphical, tabulated, and raw forms"},
    {'id': 8915, 'description': "Writing: Use syntactic structures, literary devices, and a range of vocabulary to deepen meaning and engage an intended audience with fluency"},
    {'id': 8916, 'description': "Public Speaking: Utilize a range of styles and strategies including storytelling, anecdote, argument, and exposition to achieve a self-identified goal"},
    {'id': 8931, 'description': "Engineering: Create physical and digital artifacts including circuits, machines, structures, and programs that solve real problems"},
    {'id': 8935, 'description': "Engineering: Create physical and digital artifacts including circuits, machines, structures, and programs that solve real problems"},
    {'id': 8936, 'description': "Scientific Method: Design and conduct complex experiments to test hypotheses using appropriate techniques and equipment"},
    {'id': 8944, 'description': "Beliefs: Situate a given belief system within its social, political, historical, philosophical, and religious context"},
    {'id': 8947, 'description': "Metacognition: Critique one's own performance and work, identifying strengths and weaknesses"},
    {'id': 8952, 'description': "Public Speaking: Design and deliver clear and compelling presentations that resonate with their intended audiences"},
    {'id': 8966, 'description': "Engineering: Describe how common electronic devices, mechanisms, and structures function, highlighting the key principles of engineering at work and using appropriate terms of art"},
    {'id': 8967, 'description': "Evolution: Distinguish between and describe examples from natural selection, artificial selection, and sexual selection within a single species"},
    {'id': 8963, 'description': "Engineering: Predict and explain the peformance of circuits, machines, and structures under a given set of conditions"},
    {'id': 8974, 'description': "Meaning: Describe major attempts by philosophers, political figures, religious leaders, artists, and others to offer an account of meaning"},
    {'id': 8983, 'description': "Engineering: Repurpose or hack one or more existing artifacts including hardware, software, or processes in a new way to solve a problem"},
    {'id': 8984, 'description': "Engineering: Reverse-engineer a complex mechanism, software program, or product"},
    {'id': 8989, 'description': "Engineering: Apply key elements of engineering including tension, compression, static and dynamic loads, friction, mechanical advantage, current, voltage, and resistance"},
    {'id': 8990, 'description': "Geography: Synthesize geographic knowledge to understand problems in resource conservation, environmental change, and sustainable development within the community, region, and world"},
    {'id': 9000, 'description': "Creativity: Consider input and constructive feedback when creating or refining work"},
    {'id': 9003, 'description': "System Dynamics: Analyze global-scale problems from a systems perspective, identifying the complex causal and structural relationships that create them"},
    {'id': 9004, 'description': "Sustainability: Apply key principles of sustainability including scarcity, reduction, reuse, recycle, efficiency, life cycle, opportunity cost, and externalized costs to solve problems"},
    {'id': 9007, 'description': "Sustainability: Apply key principles of sustainability including scarcity, reduction, reuse, recycle, efficiency, life cycle, opportunity cost, and externalized costs to solve problems"},
    {'id': 9008, 'description': "Engineering: Describe how common electronic devices, mechanisms, and structures function, highlighting the key principles of engineering at work and using appropriate terms of art"},
    {'id': 9013, 'description': "Research: Organize and synthesize ideas, information, and quotations from multiple sources to inform a research question or project independently"},
    {'id': 9014, 'description': "System Dynamics: Analyze global-scale problems from a systems perspective, identifying the complex causal and structural relationships that create them"},
    {'id': 9017, 'description': "Data Analysis: Record, manipulate, and evaluate experimental data to reach evidence-based conclusions"},
    {'id': 9018, 'description': "System Dynamics: Predict how a given change will either damage or benefit a system as a whole"},
    {'id': 9021, 'description': "Scientific Method: Design and conduct complex experiments to test hypotheses using appropriate techniques and equipment"},
    {'id': 9022, 'description': "Data Analysis: Utilize data as evidence to inform theory, decisions, or argument"},
    {'id': 9025, 'description': "Estimation: Use smaller intervals of time or x-values to estimate an instantaneous rate of change or tangent line slope."},
    {'id': 9026, 'description': "Algorithms: Apply arithmetic operations to matrices in order to simplify and solve systems of equations"},
    {'id': 9027, 'description': 'Algorithms: Demonstrate an understanding of all operations on Rational Numbers with "Nice Fractions" and integers and develop an understanding of operation of Improprer Fractions, Mixed Numbers and Complex Fractions'},
    {'id': 9029, 'description': "Abstraction: Differentiate between linear and nonlinear relationships in sets of data represented graphically, numerically, and symbolically"},
    {'id': 9030, 'description': "Pattern: Understand, demonstrate ability and see purpose in solving quadratic equations with multiple strategies and methods, and to realize the unique importance of the zero product property"},
    {'id': 9031, 'description': "Pattern: Demonstrate a knowledge of the properties of the special segments of triangles (median, perpendicular bisector, altitude and midsegment) and their algebraic representations"},
    {'id': 9032, 'description': "Pattern: Demonstrate an understanding of how similarity of segments and shapes is used to compare properties of objects and scale"},
    {'id': 9033, 'description': "Pattern: Apply an understanding of volume and surface area of 3D solids to solving problems involving more complex shapes"},
    {'id': 9034, 'description': "Functions: Demonstrate an understanding of a the relationship between exponential and logarithmic functions in order to graph the functions and solve equations"},
    {'id': 9035, 'description': "Functions: Develop and demonstrate an understanding of sinusoidal and periodic functions including the nature of circular trigonometric functions and their inverses."},
    {'id': 9036, 'description': "Pattern: Explore patterns for infinite sequences and series including geometric, arithmetic and others."},
    {'id': 9037, 'description': "Abstraction: Demonstrate an understanding of the properties of logarithms and their operations by simplifying logarithmic expressions"},
    {'id': 9044, 'description': "Algorithms: Demonstrate an understanding of different strategies for solving multi-step linear equations, including the use of multiplicative and additive inverses, the complement principle and the distributive property."},
    {'id': 9045, 'description': "Pattern: Demonstrate an understanding of the Pythagorean concept of distance on a plane and applications of the theorem"},
    {'id': 9046, 'description': "Pattern: Demonstrate understanding of polygon properties, including area, through applications of triangles and quadrilaterals"},
    {'id': 9047, 'description': "Pattern: Demonstrate an understanding of the properties of parallelism and perpendicularity, and how they can be used to inform theorems about quadrilaterals and distance"},
    {'id': 9048, 'description': "Algorithms: Apply an understanding of trigonometric principles to non-right triangles"},
    {'id': 9049, 'description': "Functions: Understand the applications of the three primary trigonometric functions (and their inverses) that are defined by right triangles"},
    {'id': 9050, 'description': "Abstraction: Apply trigonometric knowledge to the coordinate plane relative to a parametrized unit circle to represent circular motion creating graphical model of the function (including inverse trigonometric functions)"},
    {'id': 9039, 'description': "Abstraction & Measurement: Utilize the limit of a difference quotient to define the derivative of a function, thereby connecting the abstract concept of slope at a point, with the numerical value of the slope of a tangent line."},
    {'id': 9040, 'description': "Abstraction: Demonstrate an understanding of the properties of logarithms and of the logarithm function, including solving equations"},
    {'id': 9041, 'description': "Pattern: Order and compare rational numbers using a number line and symbols"},
    {'id': 9042, 'description': "Data Analysis: Interpret data displays, dot plot, histograms and box plot"},
    {'id': 9052, 'description': "Algorithms: Derive the rules of derivatives for all functions in order to solve problems that require the information that first and second derivatives facilitate in mathematics and science"},
    {'id': 9053, 'description': "Data Analysis: Recognize a set of data or function as modeled by an exponential function in context, whether it be growth or decay"},
    {'id': 9054, 'description': "Algorithms: Develop an understanding of the concepts of least common multiple, greatest common factor, prime numbers and prime factorization. Calculuate the LCM and GCF for a pair of numbers by finding the prime factorization"},
    {'id': 9056, 'description': "Functions: Demonstrate the ability to solve 1- and 2-variable linear inequalities, as well as absolute value inequalities and represent their solutions on a number line or the coordinate plane with correct notation, symbolically and graphically"},
    {'id': 9057, 'description': "Modeling: Appropriate use parametric equations to model linear motion with vectors"},
    {'id': 9058, 'description': "Pattern: Demonstrate an understanding of the Pythagorean concept of distance on a plane and applications of the theorem"},
    {'id': 9059, 'description': "Pattern: Demonstrate a knowledge of the properties of the special segments of triangles (median, perpendicular bisector, altitude and midsegment) and their algebraic representations"},
    {'id': 9060, 'description': "Abstraction: Apply arithmetic operations to matrices in order to simplify and solve systems of equations"},
    {'id': 9061, 'description': "Pattern: By using generalized rules of functions, make predictions on an unknown function based on patterns for all functions."},
    {'id': 9062, 'description': "Abstraction: Demonstrate ways to transform graphs of trigonometric and other functions on the Cartesian Plane"},
    {'id': 9068, 'description': "Functions: Construct linear equations, inequalities, absolute value equations, quadratic equations and their graphs from concrete and abstract sources in order to solve problems."},
    {'id': 9069, 'description': "Pattern: Demonstrate an understanding of the transformations of geometric shapes in a coordinate plane, including translsation, reflection, rotation and dilation"},
    {'id': 9070, 'description': "Pattern: Demonstrate an understanding of how similarity of segments and shapes is used to compare properties of objects and scale"},
    {'id': 9071, 'description': "Pattern: Develop a deep understanding of the special right triangles that lead to concepts in trigonometry"},
    {'id': 9072, 'description': "Functions: Demonstrate an understanding of a the relationship between exponential and logarithmic functions in order to graph the functions and solve equations"},
    {'id': 9074, 'description': "Probability: Perform calculations on a variety of complex, different probability problems including random walks, multiple dice rolled, choice and rearrangement"},
    {'id': 9075, 'description': "Algorithms: Use knowledge of different properties of functions (odd, even, periodic, inverse, transformations, etc.) to analyze other general properties."},
    {'id': 9064, 'description': "Modeling: Demonstrate an understanding of the application of implicit differentiation to relate rates of objects in real-life situations in order to solve for measurements or other rates"},
    {'id': 9065, 'description': "Modeling: Utilize mathematical methods to determine the zero-residual line, median-median line and least-squares line of a set of data and compare the appropriateness of each of the linear models."},
    {'id': 9066, 'description': 'Algorithms: Recognize and simplify ratios that are equivalent fractions, have a common factor or have "friendly" LCM up to 100.'},
    {'id': 9078, 'description': "Functions: Demonstrate an understanding of antiderivatives as the family of functions that all differ by a constant whose derivative is the given function."},
    {'id': 9079, 'description': "Probability: Calculate the probabilities and number of counts of many different types of problems including random selection, with/out replacement, random walks, multiple dice rolled, choice and rearrangement."},
    {'id': 9080, 'description': "Algorithms: Equate and represent ratios and proportions in a variety of ways, including decimals, equivalent fractions, percentages and rates of change"},
    {'id': 9082, 'description': "Measurement: Demonstrate understanding of an average rate of change as a linear rate of change numerically and graphically as slope and in context"},
    {'id': 9084, 'description': "Pattern: Demonstrates a knowledge of the properties of triangles and the appropriate application of the criteria for triangle congruence to properties of quadrilaterals and other polygons"},
    {'id': 9085, 'description': "Pattern: Demonstrate an understanding of the properties of parallelism and perpendicularity, and how they can be used to inform theorems about quadrilaterals and distance"},
    {'id': 9086, 'description': "Pattern: Demonstrate understanding of polygon properties, including area, through applications of triangles and quadrilaterals"},
    {'id': 9088, 'description': "Abstraction: Apply trigonometric knowledge to the coordinate plane relative to a unit circle to represent circular motion"},
    {'id': 9089, 'description': "Measurement: Develop an intuitive, numerical and graphical understanding of instantaneous rate of change as it pertains to real-life problems and graphical interpretation of functions."},
    {'id': 9090, 'description': "Data Analysis: Investigate limits, average rate of change, and other calculus topics with data collected numerically on very small intervals in order to draw conclusions about trends"},
    {'id': 9094, 'description': "Abstraction: Demonstrate an accurate interpretation of an antiderivative as an accumulation function of a phenomena that can then be represented as the sum of a product in a real-life context often as volume or distance."},
    {'id': 9096, 'description': "Probability: Experiment with, study and visually describe random walks, binomial situations and their relationship to combinations and Pascal’s Triangle"},
    {'id': 9098, 'description': "Measurement: Apply understanding of unit price, conversion ratios, focus on units and effective strategy to solve for specific units."},
    {'id': 9101, 'description': "Modeling: Demonstrate the ability to translate verbal descriptions into a mathematical model that represents that description(graphical, symbolic, verbal, numerical)"},
    {'id': 9102, 'description': "Pattern: Demonstrate an understanding of the properties of parallelism and perpendicularity, and how they can be used to inform theorems about quadrilaterals and distance"},
    {'id': 9103, 'description': "Pattern: Develop a deep understanding of the special right triangles that lead to concepts in trigonometry"},
    {'id': 9104, 'description': "Pattern: Demonstrate an understanding of the Pythagorean concept of distance on a plane and applications of the theorem"},
    {'id': 9105, 'description': "Abstraction & Measurement: Utilize the limit of a difference quotient to define the derivative of a function, thereby connecting the abstract concept of slope at a point, with the numerical value of the slope of a tangent line"},
    {'id': 9112, 'description': "Modeling: Utilize a linear model to predict future values and evaluate the precision of the prediction"},
    {'id': 9113, 'description': "Pattern: Demonstrate an understanding of the transformations of geometric shapes in a coordinate plane, including translsation, reflection, rotation and dilation"},
    {'id': 9114, 'description': "Pattern: Demonstrate an understanding of the transformations of geometric shapes in a coordinate plane, including translation, reflection, rotation and dilation"},
    {'id': 9115, 'description': "Pattern: Create and interpret the slope fields of a differential equation recognizing the patterns that give the family of solutions or a graph of a particular solution given an initial condition"},
    {'id': 9117, 'description': "Data Analysis: Utilize technological tools to find the curve of best fit for a set of data and visualize data."},
    {'id': 9119, 'description': "Estimation: Apply estimating to solve problems with benchmark percents"},
    {'id': 9107, 'description': "Algorithms: Interpret the process of solving a separable differential equation as antidifferentiating with respect to an independent variable with an initial condition or as a family of curves"},
    {'id': 9108, 'description': "Modeling: Use bar models to solve ratio problems given a table of data, part and whole values or part/part values."},
    {'id': 9121, 'description': "Estimation: Display an understanding of Euler’s Method to estimate a particular solution to a differential equation and describe its reasonableness"},
    {'id': 9124, 'description': "Abstraction: Interpret and derive an analytical understanding of the First and Second Fundamental Theorems of Calculus and its uses in solving appropriate problems"},
    {'id': 9126, 'description': "Modeling: Create and utilize models of three-dimensional solids in order to write integral expressions representing their volumes"},
    {'id': 9128, 'description': "Abstraction: Demonstrate an understanding of the meaning and application of first and second derivatives as a general function and the information that gives about the function of which it is the derivative"},
    {'id': 9130, 'description': "Planning: Manage time effectively, balancing multiple personal and school-related activities at once"},
    {'id': 9132, 'description': "Planning: Manage time effectively, balancing multiple personal and school-related activities at once"},
    {'id': 9134, 'description': "Creativity: Consider input and constructive feedback when creating or refining work"},
    {'id': 9135, 'description': "Modeling: Create and utilize models of three-dimensional solids in order to write integral expressions representing their volumes 1"},
    {'id': 9138, 'description': "Abstraction: Interpret and derive an analytical understanding of the First and Second Fundamental Theorems of Calculus and its uses in solving appropriate problems 1"},
    {'id': 9139, 'description': "Abstraction: Demonstrate an understanding of the meaning and application of first and second derivatives as a general function and the information that gives about the function of which it is the derivative 1"},
    {'id': 9140, 'description': "Planning: Manage time effectively, balancing multiple personal and school-related activities at once 1"},
    {'id': 9141, 'description': "Planning: Manage time effectively, balancing multiple personal and school-related activities at once 1"},
    {'id': 9147, 'description': "Creativity: Consider input and constructive feedback when creating or refining work 1"},
    {'id': 9149, 'description': "Public Speaking: Manage anxiety during public presentations"},
    {'id': 9151, 'description': "Reading: Leverage technological tools to support vocabulary-building, comprehension, and translation"},
    {'id': 9153, 'description': "Empathy: Experience others directly without prejudgment or prejudice, considering their perspective and point of view in earnest"},
    {'id': 9154, 'description': "Empathy: Experience others directly without prejudgment or prejudice, considering their perspective and point of view in earnest"},
    {'id': 9155, 'description': "Abstraction: Analyze a given thing using symbolic, visual, numerical, and verbal representations"},
    {'id': 9157, 'description': "Abstraction: Analyze a given thing using symbolic, visual, numerical, and verbal representations"},
    {'id': 9159, 'description': "Reasoning: Craft an argument that supports a claim using clear reasoning and sound evidence"},
    {'id': 9161, 'description': "Planning: Manage time effectively, balancing multiple personal and school-related activities at once"},
    {'id': 9169, 'description': "Trustworthiness: Establish trust by making good on one's commitments and delivering upon one's word"},
    {'id': 9170, 'description': "Humility: Be willing to admit mistakes and limitations and learn from them"},
    {'id': 9171, 'description': "Abstraction: Evaluate ideas using abstract methods in order to determine merit, meaning, and reasonableness"},
    {'id': 9172, 'description': "Abstraction: Evaluate ideas using abstract methods in order to determine merit, meaning, and reasonableness"},
    {'id': 9173, 'description': "Reasoning: Craft an argument that supports a claim using clear reasoning and sound evidence"},
    {'id': 9174, 'description': "Meaning: Evaluate competing or contradictory interpretations of a given artifact"},
    {'id': 9175, 'description': "Critical Thinking: Analyze the sufficiency of the evidence in support of a claim"},
    {'id': 9163, 'description': "Writing: Write at a college level in a range of styles including academic argument, research essay, textual analysis, lab report, and technical writing"},
    {'id': 9164, 'description': "Writing: Write at a college level in a range of styles including academic argument, research essay, textual analysis, lab report, and technical writing"},
    {'id': 9165, 'description': "Discussion: Engage in and contribute to conversations on prompted or familiar topics"},
    {'id': 9177, 'description': "Critical Thinking: Analyze the sufficiency of the evidence in support of a claim"},
    {'id': 9178, 'description': "Critical Thinking: Analyze the sufficiency of the evidence in support of a claim"},
    {'id': 9179, 'description': "Trustworthiness: Commit to goals and see them through to accomplishment"},
    {'id': 9181, 'description': "Metacognition: Critique one's own performance and work, identifying strengths and weaknesses"},
    {'id': 9182, 'description': "Discussion: Synthesize multiple perspectives and discussion points in one's own words"},
    {'id': 9183, 'description': "Metacognition: Monitor and reflect upon one's emotions, thoughts, and behaviors and make adjustments as needed to achieve greater levels of productivity, happiness, and health"},
    {'id': 9184, 'description': "Metacognition: Monitor and reflect upon one's emotions, thoughts, and behaviors and make adjustments as needed to achieve greater levels of productivity, happiness, and health"},
    {'id': 9185, 'description': "Meaning: Evaluate competing or contradictory interpretations of a given artifact"},
    {'id': 9186, 'description': "Planning: Manage time effectively, balancing multiple personal and school-related activities at once"},
    {'id': 9187, 'description': "Reasoning: Craft an argument that supports a claim using clear reasoning and sound evidence"},
    {'id': 9189, 'description': "Trustworthiness: Commit to goals and see them through to accomplishment"},
    {'id': 9190, 'description': "Trustworthiness: Commit to goals and see them through to accomplishment"},
    {'id': 9191, 'description': "Critical Thinking: Identificar evidências formais e de conteúdo e discutir as respectivas relevâncias."},
    {'id': 9192, 'description': "Critical Thinking: Analisar e avaliar o tipo, a fonte e a confiabilidade das evidências."},
    {'id': 9202, 'description': "Metacognition: Empenhar-se em debates reflexivos, identificando funções e qualidades de uma conversação efetiva."},
    {'id': 9198, 'description': "Planning: Organizar um portfólio de trabalhos que ilustram seleção cuidadosa de estilos e gêneros."},
    {'id': 9199, 'description': "Planning: Organizar um portfólio de trabalhos que ilustram seleção cuidadosa de estilos e gêneros."},
    {'id': 9208, 'description': "Reading: Parafrasear trechos de textos ou discussões para fazer inferências e evitando o plágio."},
    {'id': 9209, 'description': "Reading: Parafrasear trechos de textos ou discussões para fazer inferências e evitando o plágio."},
    {'id': 9211, 'description': "Planning: Organizar um portfólio de trabalhos que ilustram seleção cuidadosa de estilos e gêneros."},
    {'id': 9219, 'description': "Reading: Envolver-se com leituras literárias que possibilitem o desenvolvimento do senso estético, valorizando a literatura e outras manifestações artístico-culturais em suas dimensões lúdicas, de imaginário e encantamento, bem como reconhecendo o potencial transformador e humanizador da experiência da leitura."},
    {'id': 9217, 'description': "Writing: Produzir textos de diferentes gêneros, considerando:- adequação ao contexto produção;- adequação à forma escrita;- uso da norma culta;- expressão da própria subjetividade e voz;"},
    {'id': 9224, 'description': "Culture: Descrever as tradições, valores, comportamentos, acordos sociais e origens de determinada cultura."},
    {'id': 9225, 'description': "Culture: Descrever as tradições, valores, comportamentos, acordos sociais e origens de determinada cultura."},
    {'id': 9227, 'description': "Reading: Transferir os conhecimentos adquiridos para leitura e escrita autônoma e aplicar os gêneros literários em contextos de linguagem que transcendem a disciplina de Português."},
    {'id': 9233, 'description': "Writing: Aprimorar a análise linguística ou semiótica sobre o sistema de escrita, o sistema da língua e a norma-padrão em textos de diferentes linguagens e estilos."},
    {'id': 9238, 'description': "Writing: Desenvolver uma narrativa com a estrutura e progressão completa em um dado contexto e/ou uma sequência argumentativa com processo lógico e ideias consistentes."},
    {'id': 9254, 'description': "Produzir textos de diferentes gêneros, considerando: - adequação ao contexto produção; - adequação à forma escrita; - uso da norma culta; - expressão da própria subjetividade e voz; - utilização de estratégias de planejamento, revisão e reescrita."},
    {'id': 9259, 'description': "Writing: Produzir textos de diferentes gêneros, considerando:- adequação ao contexto produção;"},
    {'id': 9341, 'description': "Planning: Design a plan independently by starting with the end goal and delineating the steps that will lead up to it"},
    {'id': 8830, 'description': "Creativity: Create original expressions of emotion, experience, and thought"},
    {'id': 8657, 'description': "Creativity: Apply idea creation techniques including ideation and brainstorming to independently develop multiple solutions to a given problem"},
    {'id': 8664, 'description': "Creativity: Create original expressions of emotion, experience, and thought"},
    {'id': 8655, 'description': "Creativity: Consider input and constructive feedback when creating or refining work"},
    {'id': 8645, 'description': "Reasoning: Analyze arguments presented in different forms including essays, speeches, editorials, graphs, and proofs"},
    {'id': 8641, 'description': "Reading: Summarize the main ideas in high school-level texts from a variety of disciplines"},
    {'id': 8636, 'description': "Pattern: Analyze patterns in data, shapes, descriptions, equations, graphs, narrative, and verse"},
    {'id': 8723, 'description': "Metacognition: Critique one's own performance and work, identifying strengths and weaknesses"},
    {'id': 8710, 'description': "Reading: Situate a given text within the context of its creation"},
    {'id': 8706, 'description': "Reading: Leverage technological tools to support vocabulary-building, comprehension, and translation"},
    {'id': 8795, 'description': "Humility: Articulate how one's ideas and contributions build upon those of others, both past and present"},
    {'id': 8905, 'description': "Identity: Identify one's personal growth goals and areas of passion including how they contribute to a healthy sense of self"},
    {'id': 9342, 'description': "Metacognition: Critique one's own performance and work, identifying strengths and weaknesses"},
    {'id': 9343, 'description': "Creativity: Create original expressions of emotion, experience, and thought"},
    {'id': 8907, 'description': "Public Speaking: Design and deliver clear and compelling presentations that resonate with their intended audiences"},
    {'id': 8857, 'description': "Meaning: Explain the relationship between meaning and context using examples to describe how a given thing can mean differently depending on historical moment, geographical location, and personal or collective experience"},
    {'id': 8776, 'description': "Writing: Proofread the structure and grammar of one's own and others' writing"},
    {'id': 8720, 'description': "Metacognition: Critique one's own performance and work, identifying strengths and weaknesses"},
    {'id': 8772, 'description': "Writing: Proofread the structure and grammar of one's own and others' writing"},
    {'id': 9346, 'description': "Abstraction: Analyze a given thing using symbolic, visual, numerical, and verbal representations"},
    {'id': 8730, 'description': "Metacognition: Critique one's own performance and work, identifying strengths and weaknesses"},
    {'id': 8786, 'description': "Planning: Design a plan independently by starting with the end goal and delineating the steps that will lead up to it"},
    {'id': 8835, 'description': "Writing: Leverage technological tools to support grammar, spelling, vocabulary use, and translation"},
    {'id': 8839, 'description': "Writing: Use syntactic structures, literary devices, and a range of vocabulary to deepen meaning and engage an intended audience with fluency"},
    {'id': 9344, 'description': "Meaning: Explain the relationship between meaning and context using examples to describe how a given thing can mean differently depending on historical moment, geographical location, and personal or collective experience"},
    {'id': 8949, 'description': "Pattern: Use appropriate methods and rules to manipulate or analyze patterns in data, shapes, descriptions, equations, graphs, narrative, and verse."},
    {'id': 9345, 'description': "Public Speaking:  Design and deliver clear and compelling presentations that resonate with their intended audiences"},
    {'id': 8894, 'description': "Writing: Communicate judiciously in common contemporary modes including social media, email, and texting"},
    {'id': 8898, 'description': "Public Speaking: Design and deliver clear and compelling presentations that resonate with their intended audiences"},
    {'id': 8848, 'description': "Public Speaking: Utilize a range of styles and strategies including storytelling, anecdote, argument, and exposition to achieve a self-identified goal"},
    {'id': 8788, 'description': "Aesthetics: Apply aesthetic knowledge to create visual aids, documents, and decks"},
    {'id': 9446, 'description': "Reading: Summarize the main ideas in college-level texts from a variety of disciplines"},
    {'id': 9445, 'description': "Reading: Summarize the main ideas in college-level texts from a variety of disciplines"},
    {'id': 9441, 'description': "Writing: Use syntactic structures, literary devices, and a range of vocabulary to deepen meaning and engage an intended audience"},
    {'id': 9424, 'description': "Aesthetics: Recognize the value of creativity, self-expression, imagination, and originality"},
    {'id': 8850, 'description': "Meaning: Explain the relationship between meaning and context using examples to describe how a given thing can mean differently depending on historical moment, geographical location, and personal or collective experience"},
    {'id': 8939, 'description': "Discussion: Converse with others in familiar styles and contexts"},
    {'id': 8943, 'description': "Public Speaking: Utilize presentation software and multimedia to augment presentations"},
    {'id': 8970, 'description': "Discussion: Engage in and contribute to conversations on prompted or familiar topics"},
    {'id': 8973, 'description': "Discussion: Engage in and contribute to conversations on complex topics"},
    {'id': 9425, 'description': "Entrepreneurship: Design and develop a business plan and pitch deck"},
    {'id': 9442, 'description': "Public Speaking: Design and deliver clear and compelling presentations that resonate with their intended audiences"},
    {'id': 9444, 'description': "Writing: Use syntactic structures, literary devices, and a range of vocabulary to deepen meaning and engage an intended audience"},
    {'id': 9426, 'description': "Design: Apply principles of design to create a new artifact or enhance the performance of an existing one"},
    {'id': 8993, 'description': "Discussion: Summarize discussion points in one's own words to confirm meaning and intent"},
    {'id': 8644, 'description': "Research: Apply multiple citation styles including MLA, APA, and CMS"},
    {'id': 8709, 'description': "Research: Organize and synthesize ideas, information, and quotations from multiple sources to inform a research question or project independently"},
    {'id': 9427, 'description': "Design: Use digital technologies, fabrication, and processing tools to design and produce an artifact"},
    {'id': 9369, 'description': "Public Speaking: Design and deliver clear and compelling presentations"},
    {'id': 9428, 'description': "Global Trends: Analyze data and statistics to draw conclusions about global patterns, directions, and impact"},
    {'id': 8775, 'description': "Classic Works: Analyze the stylistic strengths of a given classic"},
    {'id': 8838, 'description': "System Dynamics: Analyze global-scale problems from a systems perspective, identifying the complex causal and structural relationships that create them"},
    {'id': 9429, 'description': "Research: Leverage search engines, databases, libraries, and archives independently and as appropriate to access information that answers a wide range of given and self-identified questions"},
    {'id': 9430, 'description': "Research: Organize and synthesize ideas, information, and quotations from multiple sources to inform a research question or project independently"},
    {'id': 8897, 'description': "National History: Interpret past events in their historical, cultural, social, and political contexts"},
    {'id': 8942, 'description': "Data Analysis: Utilize data as evidence to inform theory, decisions, or argument"},
    {'id': 9431, 'description': "Sustainability: Analyze the social, technological, economic, environmental, and political factors that impact sustainable practices and solutions"},
    {'id': 9440, 'description': "Reading: Summarize the main ideas in high school-level texts from a variety of disciplines"},
    {'id': 8948, 'description': "Metacognition: Critique one's own performance and work, identifying strengths and weaknesses"},
    {'id': 8945, 'description': "Beliefs: Situate a given belief system within its social, political, historical, philosophical, and religious context"},
    {'id': 8964, 'description': "Engineering: Predict and explain the peformance of circuits, machines, and structures under a given set of conditions"},
    {'id': 8956, 'description': "Global Trends: Evaluate long-term predictions made by experts in the social and natural sciences"},
    {'id': 9001, 'description': "Creativity: Consider input and constructive feedback when creating or refining work"},
    {'id': 8997, 'description': "Research: Follow ethical and legal guidelines in acquiring, using, and citing sources, including appropriate use of paraphrase, summary, and direct quotation"},
    {'id': 9009, 'description': "Sustainability: Apply key principles of sustainability including scarcity, reduction, reuse, recycle, efficiency, life cycle, opportunity cost, and externalized costs to solve problems"},
    {'id': 9010, 'description': "Engineering: Describe how common electronic devices, mechanisms, and structures function, highlighting the key principles of engineering at work and using appropriate terms of art"},
    {'id': 8979, 'description': "Sustainability: Analyze the social, technological, economic, environmental, and political factors that impact sustainable practices and solutions"},
    {'id': 8975, 'description': "Meaning: Describe major attempts by philosophers, political figures, religious leaders, artists, and others to offer an account of meaning"},
    {'id': 8985, 'description': "Engineering: Repurpose or hack one or more existing artifacts including hardware, software, or processes in a new way to solve a problem"},
    {'id': 8986, 'description': "Engineering: Reverse-engineer a complex mechanism, software program, or product"},
    {'id': 9081, 'description': "Estimation: Decide the order of values along a number line by estimating or without exact values"},
    {'id': 9067, 'description': "Abstraction: Represent and Multiply large and small numbers using exponential notation"},
    {'id': 9076, 'description': "Algorithms: Use knowledge of different properties of functions (odd, even, periodic, inverse, transformations, etc.) to analyze other general properties."},
    {'id': 9063, 'description': "Abstraction: Demonstrate ways to transform graphs of trigonometric and other functions on the Cartesian Plane"},
    {'id': 9055, 'description': "Pattern: Apply an understanding of the absolute value of a number in order to graphically represent and visualize distance"},
    {'id': 9043, 'description': "Mental Agility: Understand and apply the conversion of fractions to decimals and vice versa"},
    {'id': 9051, 'description': "Abstraction: Apply trigonometric knowledge to the coordinate plane relative to a parametrized unit circle to represent circular motion creating graphical model of the function (including inverse trigonometric functions)"},
    {'id': 9038, 'description': "Abstraction: Demonstrate an understanding of the properties of logarithms and their operations by simplifying logarithmic expressions"},
    {'id': 9028, 'description': "Algorithms: Demonstrate an understanding of the operations on all real numbers and the relationship between real numbers on a number line, with a focus on understanding irrational numbers"},
    {'id': 9251, 'description': "Identity: Explorar o estilo pessoal na escrita, em diversos gêneros, imprimindo a subjetividade, considerando o contexto e destinatários específicos."},
    {'id': 9252, 'description': "Culture: Inferir a presença de valores sociais, culturais e humanos e de diferentes visões de mundo, em textos literários."},
    {'id': 9239, 'description': "Reading: Analisar a intertextualidade presente em textos literários, históricos, filosóficos e científicos."},
    {'id': 9234, 'description': "Reading: Cultivar e expressar o gosto pessoal na leitura considerando estilo, forma, temática e ponto de vista."},
    {'id': 9243, 'description': "Writing: Aprimorar a análise linguística ou semiótica sobre o sistema de escrita, o sistema da língua e a norma-padrão em textos de diferentes linguagens e estilos."},
    {'id': 9247, 'description': "Writing: Desenvolver uma narrativa com a estrutura e progressão completa em um dado contexto e/ou uma sequência argumentativa com processo lógico e ideias consistentes."},
    {'id': 9249, 'description': "Public Speaking: Expressar-se em público com confiança, presença física e adequada articulação vocal."},
    {'id': 9228, 'description': "Reading: Analisar como forma e a estrutura da narrativa contribuem para o significado."},
    {'id': 9220, 'description': "Confidence: Compreender a ambiguidade de significados como inerente à linguagem e incorporar essa competência à leitura crítica e à escrita criativa."},
    {'id': 9212, 'description': "Confidence: Cultivar autoconfiança e expressar as próprias ideias ao interpretar, criticar e criar textos."},
    {'id': 9204, 'description': "Planning: Retomar projetos de escrita e leitura com objetivo de aprimoramento."},
    {'id': 9193, 'description': "Critical Thinking: Citar evidências visando formular, fundamentar, criticar ou refutar afirmações baseando-se em múltiplas fontes."},
    {'id': 9188, 'description': "Reasoning: Craft an argument that supports a claim using clear reasoning and sound evidence"},
    {'id': 9180, 'description': "Mental Agility: Maintain focus and concentration on a given task for a designated period of time"},
    {'id': 9167, 'description': "Planning: Manage time effectively, balancing different activities"},
    {'id': 9176, 'description': "Critical Thinking: Analyze the sufficiency of the evidence in support of a claim"},
    {'id': 9162, 'description': "Planning: Manage time effectively, balancing multiple personal and school-related activities at once"},
    {'id': 9143, 'description': "Confidence: Develop and enact strategies to cope with ambiguity and change as needed"},
    {'id': 9122, 'description': "Functions: Solve and demonstrate an understanding of direct and indirect variation problems using algebraic, graphical and numerical methods and find the constant of variation"},
    {'id': 9110, 'description': "Abstraction: Represent, manipulate and simplify proportions in a variety of ways, including decimals, equivalent fractions, percentages and algebraic techniques"},
    {'id': 9120, 'description': "Abstraction: Understand that the change in the value of a variable over a change in time can be represented numerically, symbolically and theoretically as the average rate of change"},
    {'id': 9106, 'description': "Abstraction & Measurement: Utilize the limit of a difference quotient to define the derivative of a function, thereby connecting the abstract concept of slope at a point, with the numerical value of the slope of a tangent line"},
    {'id': 9100, 'description': "Measurement: Compare irrational and rational numbers and demonstrate an understanding that the decimal approximation of an irrational number is not as precise as the actual symbolic notations of the irrational number itself"},
    {'id': 9092, 'description': "Data Analysis: Investigate limits, average rate of change, and other calculus topics with data collected numerically on very small intervals in order to draw conclusions about trends"},
    {'id': 8903, 'description': "Trustworthiness: Commit to goals and see them through to accomplishment"},
    {'id': 8904, 'description': "Discussion: Engage in and contribute to conversations on prompted or familiar topics"},
    {'id': 8900, 'description': "Classic Works: Demonstrate familiarity with classic works of literature, art, and music both nationally and internationally"},
    {'id': 8912, 'description': "Data Analysis: Record and interpret data that is presented in graphical, tabulated, and raw forms"},
    {'id': 8932, 'description': "Engineering: Create physical and digital artifacts including circuits, machines, structures, and programs that solve real problems"},
    {'id': 8921, 'description': "Global Trends: Utilize and analyze accurate and reliable sources of global data and statistics"},
    {'id': 8860, 'description': "Engineering: Apply key elements of engineering including tension, compression, static and dynamic loads, friction, mechanical advantage, current, voltage, and resistance"},
    {'id': 8867, 'description': "Civilizations: Explain the social, technological, economic, environmental, and political challenges associated with implementing a given proposed solution to a current or future threat to civilization"},
    {'id': 8873, 'description': "Reading: Describe the context of a text's creation"},
    {'id': 8890, 'description': "Public Speaking: Manage anxiety during public presentations"},
    {'id': 8883, 'description': "Design: Use digital technologies, fabrication, and processing tools to design and produce an artifact"},
    {'id': 8877, 'description': "Discussion: Engage in and contribute to conversations on prompted or familiar topics"},
    {'id': 8841, 'description': "Research: Organize and synthesize ideas, information, and quotations from multiple sources to inform a research question or project independently"},
    {'id': 8846, 'description': "Mental Agility: Maintain focus and concentration on a given task for a designated period of time"},
    {'id': 8844, 'description': "Reasoning: Craft an argument that supports a claim using clear reasoning and sound evidence"},
    {'id': 8854, 'description': "System Dynamics: Predict how a given change will either damage or benefit a system as a whole"},
    {'id': 8831, 'description': "Creativity: Create original expressions of emotion, experience, and thought"},
    {'id': 8823, 'description': "Design: Develop prototypes to test, filter, and iterate ideas"},
    {'id': 8797, 'description': "Engineering: Create physical and digital artifacts including circuits, machines, structures, and programs that solve real problems"},
    {'id': 8792, 'description': "Economics: Use economic tools and concepts to address public policy issues including competition, environmental protection, financial regulation, innovation and intellectual property, labor law, and taxation"},
    {'id': 8784, 'description': "Metacognition: Critique one's own performance and work, identifying strengths and weaknesses"},
    {'id': 8782, 'description': "Critical Thinking: Acknowledge, respond to, and refute bias in both claims and evidence"},
    {'id': 8806, 'description': "Civilizations: Describe current and future existential threats to modern civilizations and estimate their probabilities and potential impact"},
    {'id': 8812, 'description': "Public Speaking: Design and deliver clear and compelling presentations"},
    {'id': 8816, 'description': "Writing: Demonstrate familiarity with style guidelines including MLA, APA, and CMS"},
    {'id': 8778, 'description': "Discussion: Synthesize multiple perspectives and discussion points in one's own words"},
    {'id': 8768, 'description': "Metacognition: Critique one's own performance and work, identifying strengths and weaknesses"},
    {'id': 8749, 'description': "Writing: Write at a high school level in a range of styles including academic argument, research essay, textual analysis, and lab report"},
    {'id': 8759, 'description': "Design: Utilize techniques including empathy interviews, ideation and brainstorming, prototyping, testing solutions, and iterating"},
    {'id': 8741, 'description': "National History: Interpret past events in their historical, cultural, social, and political contexts"},
    {'id': 8712, 'description': "Reasoning: Analyze arguments presented in different forms including essays, speeches, editorials, graphs, and proofs"},
    {'id': 8718, 'description': "Reasoning: Present different and opposing positions with equal skill"},
    {'id': 8716, 'description': "Writing: Proofread the structure and grammar of one's own and others' writing"},
    {'id': 8727, 'description': "Research: Organize and synthesize ideas, information, and quotations from multiple sources to inform a research question or project independently"},
    {'id': 8733, 'description': "Sustainability: Analyze the social, technological, economic, environmental, and political factors that impact sustainable practices and solutions"},
    {'id': 8647, 'description': "Critical Thinking: Analyze the sufficiency of the evidence in support of a claim"},
    {'id': 8637, 'description': "Pattern: Analyze patterns in data, shapes, descriptions, equations, graphs, narrative, and verse"},
    {'id': 8629, 'description': "Design: Create a design brief that defines background, goals, timeline, constraints, and deliverables"},
    {'id': 8651, 'description': "Research: Leverage search engines, databases, libraries, and archives independently and as appropriate to access information that answers a wide range of given and self-identified questions"},
    {'id': 8653, 'description': "Empathy: Take the perspectives of individuals, groups, and cultures into account and describe their points of view"},
    {'id': 8661, 'description': "Public Speaking: Design and deliver clear and compelling presentations that resonate with their intended audiences"},
    {'id': 8702, 'description': "Confidence: Evaluate one’s own confidence across a wide range of situations and adjust accordingly as appropriate"},
    {'id': 8684, 'description': "Reading: Summarize the main ideas in high school-level texts from a variety of disciplines"},
    {'id': 8694, 'description': "Design: Conduct user research to identify and explain needs and problems"},
    {'id': 8667, 'description': "Research: Present research findings utilizing discipline-appropriate conventions"},
    {'id': 8676, 'description': "Civilizations: Describe the history of major civilizations including when, where, why, and how they first emerged"},
    {'id': 8658, 'description': "Creativity: Apply idea creation techniques including ideation and brainstorming to independently develop multiple solutions to a given problem"},
    {'id': 8656, 'description': "Creativity: Consider input and constructive feedback when creating or refining work"},
    {'id': 8649, 'description': "Creativity: Create original expressions of emotion, experience, and thought"},
    {'id': 8642, 'description': "Reading: Summarize the main ideas in high school-level texts from a variety of disciplines"},
    {'id': 8631, 'description': "Scientific Method: Construct a testable hypothesis based on observed phenomena with guidance"},
    {'id': 9412, 'description': "Physical health: Demonstrate endurance, strength, flexibility, balance, speed, and agility when performing common activities"},
    {'id': 9415, 'description': "Physical health: Demonstrate endurance, strength, flexibility, balance, speed, and agility when performing common activities"},
    {'id': 9418, 'description': "National History: Analyze the key social, political, and intellectual changes that characterize national history"},
    {'id': 9403, 'description': "Physical health: Demonstrate endurance, strength, flexibility, balance, speed, and agility when performing common activities"},
    {'id': 9406, 'description': "Physical health: Demonstrate endurance, strength, flexibility, balance, speed, and agility when performing common activities"},
    {'id': 9409, 'description': "Physical health: Demonstrate endurance, strength, flexibility, balance, speed, and agility when performing common activities"},
    {'id': 9393, 'description': "Reading: Summarize the main ideas in high school-level texts from a variety of disciplines"},
    {'id': 9347, 'description': "Creativity: Create original expressions of emotion, experience, and thought"},
    {'id': 9375, 'description': "Reading: Summarize the main ideas in high school-level texts from a variety of disciplines"},
    {'id': 9384, 'description': "Reading: Summarize the main ideas in high school-level texts from a variety of disciplines"},
    {'id': 9385, 'description': "Reading: Leverage technological tools to support vocabulary-building, comprehension, and translation"},
    {'id': 9376, 'description': "Reading: Leverage technological tools to support vocabulary-building, comprehension, and translation"},
    {'id': 9348, 'description': "Pattern: Analyze patterns in data, shapes, descriptions, equations, graphs, narrative, and verse"},
    {'id': 9394, 'description': "Reading: Leverage technological tools to support vocabulary-building, comprehension, and translation"},
    {'id': 9410, 'description': "Mental health: Be aware of one’s emotions, thoughts, and behaviors and react in appropriate ways across a range of situations"},
    {'id': 9407, 'description': "Mental health: Be aware of one’s emotions, thoughts, and behaviors and react in appropriate ways across a range of situations"},
    {'id': 9404, 'description': "Mental health: Be aware of one’s emotions, thoughts, and behaviors and react in appropriate ways across a range of situations"},
    {'id': 9416, 'description': "Mental health: Be aware of one’s emotions, thoughts, and behaviors and react in appropriate ways across a range of situations"},
    {'id': 9413, 'description': "Mental health: Be aware of one’s emotions, thoughts, and behaviors and react in appropriate ways across a range of situations"},
    {'id': 9015, 'description': "Culture: Analyze the traditions, values, behaviors, social agreements, and origins of a range of cultures, including one's own"},
    {'id': 8724, 'description': "Metacognition: Critique one's own performance and work, identifying strengths and weaknesses"},
    {'id': 8714, 'description': "Pattern: Analyze patterns in data, shapes, descriptions, equations, graphs, narrative, and verse"},
    {'id': 8696, 'description': "Life: Describe how different conditions and climates support different kinds of life"},
    {'id': 8707, 'description': "Reading: Leverage technological tools to support vocabulary-building, comprehension, and translation"},
    {'id': 8906, 'description': "Identity: Identify one's personal growth goals and areas of passion including how they contribute to a healthy sense of self"},
    {'id': 8908, 'description': "Public Speaking: Design and deliver clear and compelling presentations that resonate with their intended audiences"},
    {'id': 8892, 'description': "Ethics: Discern and analyze ethical dilemmas across social, political, historical, philosophical, and religious contexts"},
    {'id': 8780, 'description': "Abstraction: Analyze a given thing using symbolic, visual, numerical, and verbal representations"},
    {'id': 8721, 'description': "Metacognition: Critique one's own performance and work, identifying strengths and weaknesses"},
    {'id': 8761, 'description': "Ecosystems: Describe the impact of changes in biodiversity upon a given ecosystem"},
    {'id': 8773, 'description': "Writing: Proofread the structure and grammar of one's own and others' writing"},
    {'id': 9414, 'description': "Mental health: Identify and describe high-risk behaviors including their effects on the well-being of oneself and of others"},
    {'id': 9417, 'description': "Mental health: Identify and describe high-risk behaviors including their effects on the well-being of oneself and of others"},
    {'id': 9405, 'description': "Mental health: Identify and describe high-risk behaviors including their effects on the well-being of oneself and of others"},
    {'id': 9408, 'description': "Mental health: Identify and describe high-risk behaviors including their effects on the well-being of oneself and of others"},
    {'id': 9411, 'description': "Mental health: Identify and describe high-risk behaviors including their effects on the well-being of oneself and of others"},
    {'id': 9395, 'description': "Writing: Proofread the structure and grammar of one's own and others' writing"},
    {'id': 9349, 'description': "Abstraction: Analyze a given thing using symbolic, visual, numerical, and verbal representations"},
    {'id': 9377, 'description': "Writing: Proofread the structure and grammar of one's own and others' writing"},
    {'id': 9386, 'description': "Writing: Proofread the structure and grammar of one's own and others' writing"},
    {'id': 9387, 'description': "Writing: Leverage technological tools to support grammar, spelling, vocabulary use, and translation"},
    {'id': 9378, 'description': "Writing: Leverage technological tools to support grammar, spelling, vocabulary use, and translation"},
    {'id': 9396, 'description': "Writing: Leverage technological tools to support grammar, spelling, vocabulary use, and translation"},
    {'id': 8704, 'description': "Global Trends: Trace a given social, political, or environmental pattern across a range of geographical regions and over a long historical arc"},
    {'id': 8787, 'description': "Planning: Design a plan independently by starting with the end goal and delineating the steps that will lead up to it"},
    {'id': 8836, 'description': "Writing: Leverage technological tools to support grammar, spelling, vocabulary use, and translation"},
    {'id': 8825, 'description': "Scientific Method: Collect, represent, and evaluate experimental data to draw evidence-based conclusions"},
    {'id': 8950, 'description': "Pattern: Use appropriate methods and rules to manipulate or analyze patterns in data, shapes, descriptions, equations, graphs, narrative, and verse."},
    {'id': 9019, 'description': "National History: Connect contemporary challenges and events to similar challenges and events in national history"},
    {'id': 8849, 'description': "Public Speaking: Utilize a range of styles and strategies including storytelling, anecdote, argument, and exposition to achieve a self-identified goal"},
    {'id': 8789, 'description': "Aesthetics: Apply aesthetic knowledge to create visual aids, documents, and decks"},
    {'id': 8885, 'description': "Earth: Describe how human activities have altered the biosphere"},
    {'id': 8895, 'description': "Writing: Communicate judiciously in common contemporary modes including social media, email, and texting"},
    {'id': 9397, 'description': "Writing: Communicate judiciously in common contemporary modes including social media, email, and texting"},
    {'id': 9379, 'description': "Writing: Communicate judiciously in common contemporary modes including social media, email, and texting"},
    {'id': 9388, 'description': "Writing: Communicate judiciously in common contemporary modes including social media, email, and texting"},
    {'id': 9389, 'description': "Discussion: Converse with others in familiar styles and contexts"},
    {'id': 9380, 'description': "Discussion: Converse with others in familiar styles and contexts"},
    {'id': 9398, 'description': "Discussion: Converse with others in familiar styles and contexts"},
    {'id': 9432, 'description': "Aesthetics: Recognize the value of creativity, self-expression, imagination, and originality"},
    {'id': 8934, 'description': "Planning: Design a plan with guidance by starting with the end goal and delineating the steps that will lead up to it"},
    {'id': 8851, 'description': "Meaning: Explain the relationship between meaning and context using examples to describe how a given thing can mean differently depending on historical moment, geographical location, and personal or collective experience"},
    {'id': 8940, 'description': "Discussion: Converse with others in familiar styles and contexts"},
    {'id': 8968, 'description': "National History: Explain how citizens participate in the political process at local, regional, and national levels"},
    {'id': 8971, 'description': "Discussion: Engage in and contribute to conversations on prompted or familiar topics"},
    {'id': 8833, 'description': "National History: Interpret past events in their historical, cultural, social, and political contexts"},
    {'id': 9433, 'description': "Entrepreneurship: Design and develop a business plan and pitch deck"},
    {'id': 9399, 'description': "Discussion: Engage in and contribute to conversations on prompted or familiar topics"},
    {'id': 9381, 'description': "Discussion: Engage in and contribute to conversations on prompted or familiar topics"},
    {'id': 9390, 'description': "Discussion: Engage in and contribute to conversations on prompted or familiar topics"},
    {'id': 9421, 'description': "Cells: Distinguish between plant, animal, and bacteria cells, analyzing differences and similarities in their parts and corresponding functions"},
    {'id': 9422, 'description': "Cells: Describe the structure and function of cells including specialized cells"},
    {'id': 9391, 'description': "Discussion: Summarize discussion points in one's own words to confirm meaning and intent"},
    {'id': 9382, 'description': "Discussion: Summarize discussion points in one's own words to confirm meaning and intent"},
    {'id': 9400, 'description': "Discussion: Summarize discussion points in one's own words to confirm meaning and intent"},
    {'id': 9434, 'description': "Design: Apply principles of design to create a new artifact or enhance the performance of an existing one"},
    {'id': 8991, 'description': "Pattern: Analyze patterns in history, political systems, and nature using concrete, illustrative examples"},
    {'id': 8994, 'description': "Discussion: Summarize discussion points in one's own words to confirm meaning and intent"},
    {'id': 9005, 'description': "Public Speaking: Utilize a range of styles and strategies including storytelling, anecdote, argument, and exposition to achieve a self-identified goal"},
    {'id': 9435, 'description': "Design: Use digital technologies, fabrication, and processing tools to design and produce an artifact"},
    {'id': 9401, 'description': "Public Speaking: Design and deliver clear and compelling presentations"},
    {'id': 9370, 'description': "Public Speaking: Design and deliver clear and compelling presentations"},
    {'id': 9383, 'description': "Public Speaking: Design and deliver clear and compelling presentations"},
    {'id': 9392, 'description': "Public Speaking: Design and deliver clear and compelling presentations"},
    {'id': 9423, 'description': "Data Analysis: Practice using data as evidence to inform theory, decisions, or argument"},
    {'id': 9436, 'description': "Global Trends: Analyze data and statistics to draw conclusions about global patterns, directions, and impact"},
    {'id': 9023, 'description': "Reasoning: Craft an argument that supports a claim using clear reasoning and sound evidence"},
    {'id': 8937, 'description': "Reasoning: Form judgments, beliefs, and ideas based on sound reasoning and be able to persuasively present that reasoning"},
    {'id': 9437, 'description': "Research:  Leverage search engines, databases, libraries, and archives independently and as appropriate to access information that answers a wide range of given and self-identified questions"},
    {'id': 9438, 'description': "Research: Organize and synthesize ideas, information, and quotations from multiple sources to inform a research question or project independently"},
    {'id': 8770, 'description': "Research: Organize and synthesize ideas, information, and quotations from multiple sources to inform a research question or project independently"},
    {'id': 9439, 'description': "Sustainability: Analyze the social, technological, economic, environmental, and political factors that impact sustainable practices and solutions"},
    {'id': 8996, 'description': "Sustainability: Describe the social, technological, economic, environmental, and political factors that impact sustainable practices and solutions"},
    {'id': 8779, 'description': "Discussion: Synthesize multiple perspectives and discussion points in one's own words"},
    {'id': 8769, 'description': "Metacognition: Critique one's own performance and work, identifying strengths and weaknesses"},
    {'id': 8765, 'description': "Reading: Identify and describe common syntactic and narrative structures, literary devices, and advanced vocabulary"},
    {'id': 8745, 'description': "Research: Differentiate between sources that are credible, accurate, and timely and those that are not using concrete, illustrative examples"},
    {'id': 8760, 'description': "Design: Utilize techniques including empathy interviews, ideation and brainstorming, prototyping, testing solutions, and iterating"},
    {'id': 8713, 'description': "Reasoning: Analyze arguments presented in different forms including essays, speeches, editorials, graphs, and proofs"},
    {'id': 8719, 'description': "Planning: Manage time effectively, balancing different activities"},
    {'id': 8728, 'description': "Research: Organize and synthesize ideas, information, and quotations from multiple sources to inform a research question or project independently"},
    {'id': 8737, 'description': "Reading: Summarize the main ideas in high school-level texts from a variety of disciplines"},
    {'id': 8739, 'description': "Atoms: Describe the basic structure of an atom including protons, neutrons, and electrons"},
    {'id': 8648, 'description': "Critical Thinking: Analyze the sufficiency of the evidence in support of a claim"},
    {'id': 8638, 'description': "Pattern: Analyze patterns in data, shapes, descriptions, equations, graphs, narrative, and verse"},
    {'id': 8630, 'description': "Design: Create a design brief that defines background, goals, timeline, constraints, and deliverables"},
    {'id': 8635, 'description': "Creativity: Use guided idea creation techniques including ideation and brainstorming to develop multiple solutions to a given problem"},
    {'id': 8654, 'description': "Creativity: Use guided idea creation techniques including ideation and brainstorming to develop multiple solutions to a given problem"},
    {'id': 8662, 'description': "Public Speaking: Design and deliver clear and compelling presentations that resonate with their intended audiences"},
    {'id': 8674, 'description': "Atoms: Describe the relationship between atoms and molecules, properties of substances, states of matter, phase changes, and conservation of matter"},
    {'id': 8679, 'description': "Creativity: Create original expressions of emotion, experience, and thought"},
    {'id': 8680, 'description': "Culture: Describe the traditions, values, behaviors, social agreements, and origins of a range of cultures, including one's own"},
    {'id': 8668, 'description': "Creativity: Use guided idea creation techniques including ideation and brainstorming to develop multiple solutions to a given problem"},
    {'id': 8672, 'description': "Writing: Write at a high school level in a range of styles including academic argument, research essay, textual analysis, and lab report"},
    {'id': 8695, 'description': "Design: Conduct user research to identify and explain needs and problems"},
    {'id': 8703, 'description': "Confidence: Evaluate one’s own confidence across a wide range of situations and adjust accordingly as appropriate"},
    {'id': 8700, 'description': "Writing: Practice using a range of written narrative structures to tell real or imagined events"},
    {'id': 8832, 'description': "Creativity: Create original expressions of emotion, experience, and thought"},
    {'id': 8829, 'description': "Public Speaking: Practice using a range of styles and strategies including storytelling, anecdote, argument, and exposition to achieve a given goal"},
    {'id': 8824, 'description': "Design: Develop prototypes to test, filter, and iterate ideas"},
    {'id': 8855, 'description': "System Dynamics: Predict how a given change will either damage or benefit a system as a whole"},
    {'id': 8842, 'description': "Research: Organize and synthesize ideas, information, and quotations from multiple sources to inform a research question or project independently"},
    {'id': 8847, 'description': "Metacognition: Critique one's own performance and work, identifying strengths and weaknesses"},
    {'id': 8793, 'description': "Economics: Use economic tools and concepts to address public policy issues including competition, environmental protection, financial regulation, innovation and intellectual property, labor law, and taxation"},
    {'id': 8785, 'description': "Planning: Design a plan with guidance by starting with the end goal and delineating the steps that will lead up to it"},
    {'id': 8809, 'description': "Research: Follow ethical and legal guidelines in acquiring, using, and citing sources"},
    {'id': 8803, 'description': "Atoms: Classify objects according to properties of matter including density, mass, charge, and chemical composition"},
    {'id': 8801, 'description': "Public Speaking: Design and deliver clear and compelling presentations"},
    {'id': 8933, 'description': "Engineering: Create physical and digital artifacts including circuits, machines, structures, and programs that solve real problems"},
    {'id': 8925, 'description': "Empathy: Take the perspectives of individuals, groups, and cultures into account and describe their points of view"},
    {'id': 8919, 'description': "Chemical Reactions: Identify and differentiate between the products and reactants of different chemical reactions"},
    {'id': 8901, 'description': "Classic Works: Demonstrate familiarity with classic works of literature, art, and music both nationally and internationally"},
    {'id': 8913, 'description': "Data Analysis: Record and interpret data that is presented in graphical, tabulated, and raw forms"},
    {'id': 8888, 'description': "Classic Works: Describe the stylistic strengths of a given classic"},
    {'id': 8891, 'description': "Public Speaking: Manage anxiety during public presentations"},
    {'id': 8884, 'description': "Design: Use digital technologies, fabrication, and processing tools to design and produce an artifact"},
    {'id': 8870, 'description': "Identity: Explain and analyze constructs of gender, race, class, sexuality, religion, ability, age, ethnicity, and nationality and their intersecting relationships both historically and in the present moment"},
    {'id': 8865, 'description': "Chemical Reactions: Use the periodic table to identify the number of protons, neutrons, electrons, and atomic mass of different elements"},
    {'id': 8946, 'description': "Beliefs: Situate a given belief system within its social, political, historical, philosophical, and religious context"},
    {'id': 8965, 'description': "Engineering: Predict and explain the peformance of circuits, machines, and structures under a given set of conditions"},
    {'id': 8955, 'description': "Earth: Describe the origin, distribution, and relative abundance of the Earth’s resources"},
    {'id': 9011, 'description': "Sustainability: Apply key principles of sustainability including scarcity, reduction, reuse, recycle, efficiency, life cycle, opportunity cost, and externalized costs to solve problems"},
    {'id': 9012, 'description': "Engineering: Describe how common electronic devices, mechanisms, and structures function, highlighting the key principles of engineering at work and using appropriate terms of art"},
    {'id': 9002, 'description': "Creativity: Consider input and constructive feedback when creating or refining work"},
    {'id': 8987, 'description': "Engineering: Repurpose or hack one or more existing artifacts including hardware, software, or processes in a new way to solve a problem"},
    {'id': 8988, 'description': "Engineering: Reverse-engineer a complex mechanism, software program, or product"},
    {'id': 8976, 'description': "Meaning: Describe major attempts by philosophers, political figures, religious leaders, artists, and others to offer an account of meaning"},
    {'id': 8978, 'description': "Sustainability: Explain how the health of ecological, social, and economic systems impacts natural and human communities"},
    {'id': 9244, 'description': "Planning: Organizar um portfólio de trabalhos que ilustram seleção cuidadosa de estilos e gêneros."},
    {'id': 9235, 'description': "Reading: Interessar-se pela leitura de livros de literatura e outros gêneros, acolhendo especialmente textos que desafiem suas possibilidades atuais e suas experiências anteriores."},
    {'id': 9240, 'description': "Reading: Compreender a inter-relação entre aspectos formais de textos de vários gêneros (organização, estilo, apropriação da norma linguística) e seus leitores potenciais."},
    {'id': 9194, 'description': "Writing: Produzir textos de diferentes gêneros, considerando:"},
    {'id': 9205, 'description': "Writing: Fazer uso consciente e reflexivo da norma-padrão em situações de fala e escrita."},
    {'id': 9213, 'description': "Writing: Analisar, em narrativas ficcionais, em textos poéticos, e em textos informativos e investigativos, as diferentes formas de composição e seus respectivos efeitos de sentido."},
    {'id': 9221, 'description': "Writing: Aprimorar a análise linguística ou semiótica sobre o sistema de escrita, o sistema da língua e a norma-padrão em textos de diferentes linguagens e estilos."},
    {'id': 9229, 'description': "Writing: Aplicar os conceitos de teoria literária e linguística a narrativas de ficção e discursos não ficcionais."},
    {'id': 9327, 'description': "Creativity: Create original expressions of emotion, experience, and thought"},
    {'id': 8659, 'description': "Creativity: Apply idea creation techniques including ideation and brainstorming to independently develop multiple solutions to a given problem"},
    {'id': 8643, 'description': "Reading: Summarize the main ideas in high school-level texts from a variety of disciplines"},
    {'id': 9419, 'description': "National History: Analyze the key social, political, and intellectual changes that characterize national history"},
    {'id': 9350, 'description': "Creativity: Create original expressions of emotion, experience, and thought"},
    {'id': 9351, 'description': "Pattern: Analyze patterns in data, shapes, descriptions, equations, graphs, narrative, and verse"},
    {'id': 8725, 'description': "Metacognition: Critique one's own performance and work, identifying strengths and weaknesses"},
    {'id': 8708, 'description': "Reading: Leverage technological tools to support vocabulary-building, comprehension, and translation"},
    {'id': 9328, 'description': "Pattern: Analyze patterns in data, shapes, descriptions, equations, graphs, narrative, and verse"},
    {'id': 9016, 'description': "Culture: Analyze the traditions, values, behaviors, social agreements, and origins of a range of cultures, including one's own"},
    {'id': 9329, 'description': "Abstraction: Analyze a given thing using symbolic, visual, numerical, and verbal representations"},
    {'id': 8774, 'description': "Writing: Proofread the structure and grammar of one's own and others' writing"},
    {'id': 8893, 'description': "Ethics: Discern and analyze ethical dilemmas across social, political, historical, philosophical, and religious contexts"},
    {'id': 8909, 'description': "Public Speaking: Design and deliver clear and compelling presentations that resonate with their intended audiences"},
    {'id': 9352, 'description': "Abstraction: Analyze a given thing using symbolic, visual, numerical, and verbal representations"},
    {'id': 8896, 'description': "Writing: Communicate judiciously in common contemporary modes including social media, email, and texting"},
    {'id': 8705, 'description': "Global Trends: Trace a given social, political, or environmental pattern across a range of geographical regions and over a long historical arc"},
    {'id': 8951, 'description': "Pattern: Use appropriate methods and rules to manipulate or analyze patterns in data, shapes, descriptions, equations, graphs, narrative, and verse."},
    {'id': 9020, 'description': "National History: Connect contemporary challenges and events to similar challenges and events in national history"},
    {'id': 8790, 'description': "Aesthetics: Apply aesthetic knowledge to create visual aids, documents, and decks"},
    {'id': 8837, 'description': "Writing: Leverage technological tools to support grammar, spelling, vocabulary use, and translation"},
    {'id': 8852, 'description': "Meaning: Explain the relationship between meaning and context using examples to describe how a given thing can mean differently depending on historical moment, geographical location, and personal or collective experience"},
    {'id': 8941, 'description': "Discussion: Converse with others in familiar styles and contexts"},
    {'id': 8969, 'description': "National History: Explain how citizens participate in the political process at local, regional, and national levels"},
    {'id': 8972, 'description': "Discussion: Engage in and contribute to conversations on prompted or familiar topics"},
    {'id': 8834, 'description': "National History: Interpret past events in their historical, cultural, social, and political contexts"},
    {'id': 8992, 'description': "Pattern: Analyze patterns in history, political systems, and nature using concrete, illustrative examples"},
    {'id': 8995, 'description': "Discussion: Summarize discussion points in one's own words to confirm meaning and intent"},
    {'id': 9006, 'description': "Public Speaking: Utilize a range of styles and strategies including storytelling, anecdote, argument, and exposition to achieve a self-identified goal"},
    {'id': 9371, 'description': "Public Speaking: Design and deliver clear and compelling presentations"},
    {'id': 9024, 'description': "Reasoning: Craft an argument that supports a claim using clear reasoning and sound evidence"},
    {'id': 8938, 'description': "Reasoning: Form judgments, beliefs, and ideas based on sound reasoning and be able to persuasively present that reasoning"},
    {'id': 8771, 'description': "Research: Organize and synthesize ideas, information, and quotations from multiple sources to inform a research question or project independently"},
    {'id': 8746, 'description': "Economics: Identify basic economic concepts"},
    {'id': 8742, 'description': "Writing: Proofread the structure and grammar of one's own and others' writing"},
    {'id': 8743, 'description': "Writing: Use syntactic structures, literary devices, and a range of vocabulary to deepen meaning and engage an intended audience"},
    {'id': 8740, 'description': "Classic Works: Demonstrate familiarity with classic works of literature, art, and music both nationally and internationally"},
    {'id': 8738, 'description': "Waves: Differentiate between different types of electromagnetic waves including how the wavelength and intensity of light changes their behaviors and interactions with matter"},
    {'id': 8734, 'description': "Reading: Leverage technological tools to support vocabulary-building, comprehension, and translation"},
    {'id': 8673, 'description': "Waves: Describe and measure waves in terms of basic properties including amplitude, frequency, and wavelength"},
    {'id': 8669, 'description': "Reading: Summarize the main ideas in high school-level texts from a variety of disciplines"},
    {'id': 8681, 'description': "Sustainability: Explain key principles of sustainability including scarcity, reduction, reuse, recycle, efficiency, life cycle, opportunity cost, and externalized costs"},
    {'id': 8675, 'description': "Creativity: Create original expressions of emotion, experience, and thought"},
    {'id': 8677, 'description': "Writing: Write at a high school level in a range of styles including academic argument, research essay, textual analysis, and lab report"},
    {'id': 8798, 'description': "Research: Present research findings in a range of styles and formats"},
    {'id': 8802, 'description': "Scientific Method: Construct a testable hypothesis based on observed phenomena with guidance"},
    {'id': 8805, 'description': "Design: Use digital technologies to design and produce an artifact with guidance"},
    {'id': 8807, 'description': "Writing: Revise the purpose, tone, and genre of one's own writing to address different intended audiences"},
    {'id': 8810, 'description': "Research: Organize ideas, information, and quotations from mutliple sources to inform a research question or project with guidance"},
    {'id': 8920, 'description': "Metacognition: Critique one's own performance and work, identifying strengths and weaknesses"},
    {'id': 8923, 'description': "Research: Organize ideas, information, and quotations from mutliple sources to inform a research question or project with guidance"},
    {'id': 8918, 'description': "Scientific Method: Collect, represent, and evaluate experimental data to draw evidence-based conclusions"},
    {'id': 8866, 'description': "Aesthetics: Describe the value of wonder, awe, and beauty across a range of disciplines and experiences"},
    {'id': 8868, 'description': "Public Speaking: Design and deliver clear and compelling presentations"},
    {'id': 8871, 'description': "System Dynamics: Research and evaluate the causes of both contemporary and historical global patterns using systems dynamics frameworks"},
    {'id': 8861, 'description': "Writing: Practice using a range of written narrative structures to tell real or imagined events"},
    {'id': 8864, 'description': "Scientific Method: Design and conduct simple and complex experiments to test hypotheses with guidance"},
    {'id': 8954, 'description': "Scientific Method: Identify independent and dependent variables in a given experiment including techniques, tools, and methods of measurement"},
    {'id': 8977, 'description': "Data Analysis: Represent a data set visually"},
    {'id': 9241, 'description': "Writing: Empenhar-se no processo de escrita, aperfeiçoando os trabalhos visando publicação."},
    {'id': 9236, 'description': "Reasoning: Parafrasear evidências em textos verbais-semióticos e debates, de modo a fazer inferências e identificar argumentos, sempre evitando o plágio."},
    {'id': 9245, 'description': "Writing: Produzir textos de diferentes gêneros, considerando:a) a adequação ao contexto produção e circulação;b) a adequação à forma escrita, oral, visual, cinética etc.;"},
    {'id': 9230, 'description': "Reading: Compreender a estrutura de composição e a intencionalidade de textos de ficção, poéticos, informativos, jornalísticos e persuasivos."},
    {'id': 9222, 'description': "Writing: Aprimorar a análise linguística ou semiótica sobre o sistema de escrita, o sistema da língua e a norma-padrão em textos de diferentes linguagens e estilos."},
    {'id': 9214, 'description': "Planning: Retomar projetos de escrita e leitura com objetivo de aprimoramento."},
    {'id': 9206, 'description': "Reading: Envolver-se com leituras literárias que possibilitem o desenvolvimento do senso estético, valorizando a literatura e outras manifestações artístico-culturais em suas dimensões lúdicas, de imaginário e encantamento, bem como reconhecendo o potencial transformador e humanizador da experiência da leitura."},
    {'id': 9195, 'description': "Planning: Organizar um portfólio de trabalhos que ilustram seleção cuidadosa de estilos e gêneros."},
    {'id': 9330, 'description': "Creativity: Create original expressions of emotion, experience, and thought"},
    {'id': 9353, 'description': "Creativity: Create original expressions of emotion, experience, and thought"},
    {'id': 9354, 'description': "Pattern: Analyze patterns in data, shapes, descriptions, equations, graphs, narrative, and verse"},
    {'id': 9331, 'description': "Pattern: Analyze patterns in data, shapes, descriptions, equations, graphs, narrative, and verse"},
    {'id': 9332, 'description': "Abstraction: Analyze a given thing using symbolic, visual, numerical, and verbal representations"},
    {'id': 9355, 'description': "Abstraction: Analyze a given thing using symbolic, visual, numerical, and verbal representations"},
    {'id': 9196, 'description': "Creativity: Reformular os argumentos de uma redação para superar inconsistências e aprimorar a coesão."},
    {'id': 9207, 'description': "Writing: Produzir diferentes gêneros textuais em nível universitário, incluindo fichamentos, ensaios, comentários críticos e relatórios de pesquisa"},
    {'id': 9215, 'description': "Reading: Analisar como forma e a estrutura da narrativa contribuem para o significado."},
    {'id': 9223, 'description': "Public Speaking: Expressar-se em público com confiança, presença física e adequada articulação vocal."},
    {'id': 9231, 'description': "Criatividade: Criar formas originais de expressar emoção, experiência e pensamentos"},
    {'id': 8981, 'description': "Engineering: Apply key elements of engineering including tension, compression, static and dynamic loads, friction, mechanical advantage, current, voltage, and resistance"},
    {'id': 8998, 'description': "Algorithms: Design and debug complex algorithms to solve real-world problems using a procedural language"},
    {'id': 8959, 'description': "Scientific Method: Collect, represent, evaluate, and analyze experimental data to draw evidence-based conclusions"},
    {'id': 8961, 'description': "Reading: Explain how common syntactic and narrative structures, literary devices, and advanced vocabulary are used for rhetorical effect"},
    {'id': 8962, 'description': "Public Speaking: Utilize a range of styles and strategies including storytelling, anecdote, argument, and exposition to achieve a self-identified goal"},
    {'id': 8874, 'description': "Waves: Describe wave phenomena including reflection, refraction, diffraction, interference, polarization, and the Doppler effect"},
    {'id': 8876, 'description': "Creativity: Create original expressions of emotion, experience, and thought"},
    {'id': 8878, 'description': "Confidence: Take on leadership roles when needed and appropriate"},
    {'id': 8879, 'description': "Design: Use digital technologies, fabrication, and processing tools to design and produce an artifact"},
    {'id': 8927, 'description': "Scientific Method: Construct a testable hypothesis based on observed phenomena"},
    {'id': 8928, 'description': "Empathy: Experience others directly without prejudgment or prejudice, considering their perspective and point of view in earnest"},
    {'id': 8929, 'description': "Discussion: Engage in and contribute to conversations on complex topics"},
    {'id': 8813, 'description': "Atoms: Use atomic theory to describe properties of matter including density, mass, charge, and chemical composition"},
    {'id': 8817, 'description': "Writing: Write for a range of specified intended audiences utilizing different genres and tones effectively"},
    {'id': 8818, 'description': "Design: Develop prototypes to test, filter, and iterate ideas"},
    {'id': 8815, 'description': "Writing: Proofread the structure and grammar of one's own and others' writing"},
    {'id': 8682, 'description': "Research: Follow ethical and legal guidelines in acquiring, using, and citing sources"},
    {'id': 8685, 'description': "Atoms: Explain how all matter is composed of atoms and constituent parts whose number and arrangement determine their behavior"},
    {'id': 8687, 'description': "Writing: Use syntactic structures, literary devices, and a range of vocabulary to deepen meaning and engage an intended audience with fluency"},
    {'id': 8688, 'description': "Reading: Summarize the main ideas in college-level texts from a variety of disciplines"},
    {'id': 8689, 'description': "Trustworthiness: Commit to goals and see them through to accomplishment"},
    {'id': 8747, 'description': "National History: Situate past events in historical, cultural, social, and political contexts"},
    {'id': 8752, 'description': "Writing: Utilize a range of written narrative structures to tell real or imagined events"},
    {'id': 8753, 'description': "Reading: Analyze connections among a range of texts across literature, history, philosophy, and science"},
    {'id': 8754, 'description': "Design: Utilize techniques including empathy interviews, ideation and brainstorming, prototyping, testing solutions, and iterating"},
    {'id': 8750, 'description': "Atoms: Describe the modern model of atomic structure and the properties of its constituent parts"},
    {'id': 9333, 'description': "Creativity: Create original expressions of emotion, experience, and thought"},
    {'id': 9356, 'description': "Creativity: Create original expressions of emotion, experience, and thought"},
    {'id': 9359, 'description': "Writing: Write at a college level in a range of styles including academic argument, research essay, textual analysis, lab report, and technical writing"},
    {'id': 9360, 'description': "Reading: Summarize the main ideas in college-level texts from a variety of disciplines"},
    {'id': 9357, 'description': "Pattern: Analyze patterns in data, shapes, descriptions, equations, graphs, narrative, and verse"},
    {'id': 9334, 'description': "Pattern: Analyze patterns in data, shapes, descriptions, equations, graphs, narrative, and verse"},
    {'id': 9335, 'description': "Abstraction: Analyze a given thing using symbolic, visual, numerical, and verbal representations"},
    {'id': 9358, 'description': "Abstraction: Analyze a given thing using symbolic, visual, numerical, and verbal representations"},
    {'id': 9361, 'description': "Metacognition: Critique one's own performance and work, identifying strengths and weaknesses"},
    {'id': 9362, 'description': "Planning: Define and set specific, measurable, attainable, relevant, and timely goals"},
    {'id': 9363, 'description': "Writing: Use syntactic structures, literary devices, and a range of vocabulary to deepen meaning and engage an intended audience with fluency"},
    {'id': 9364, 'description': "Research: Organize and synthesize ideas, information, and quotations from multiple sources to inform a research question or project independently"},
    {'id': 9365, 'description': "Research: Leverage search engines, databases, libraries, and archives independently and as appropriate to access information that answers a wide range of given and self-identified questions"},
    {'id': 9366, 'description': "Discussion: Engage in and contribute to conversations on complex topics"},
    {'id': 9367, 'description': "Discussion: Synthesize multiple perspectives and discussion points in one's own words"},
    {'id': 9246, 'description': "Reading: Cultivar e expressar o gosto pessoal na leitura considerando estilo, forma, temática e ponto de vista."},
    {'id': 9250, 'description': "Public Speaking: Utilizar amplo leque de estratégias e estilos narrativos, expositivos e argumentativos, para comunicar-se e motivar os interlocutores ou a audiência."},
    {'id': 9248, 'description': "Meaning: Explicar a relação entre significado e contexto usando exemplos para descrever como uma determinada coisa pode ter significados diferentes dependendo do momento histórico, localização geográfica e experiência pessoal ou coletiva."},
    {'id': 9237, 'description': "Critical Thinking: Analisar se as evidências apresentadas são suficientes para apoiar uma proposição."},
    {'id': 9242, 'description': "Writing: Desenvolver textos expositivos com cuidado estético e clareza de ideias, precisão conceitual, e informações fundamentadas em diferentes fontes."},
    {'id': 9232, 'description': "Belief: Descrever como as experiências individuais ou coletivas podem direcionar a um sistema de crenças enquanto outro grupo ou indivíduo pode levar a um sistema de crenças completamente diferente."},
    {'id': 9226, 'description': "Planning: Elaborar um planejamento de modo independente, começando com o objetivo final e delineando os passos que levarão a esse objetivo."},
    {'id': 9218, 'description': "Metacognition: Demonstrar sensibilidade ao detalhe e compreensão cuidadosa de textos e discussões por meio de sínteses escritas ou reflexões compartilhadas oralmente."},
    {'id': 9210, 'description': "Reasoning: Criar argumentos que sustentam uma ideia, utilizando evidências claras e lógicas."},
    {'id': 9200, 'description': "Creativity: Reformular os argumentos de uma redação para superar inconsistências e aprimorar a coesão."},
    {'id': 8960, 'description': "Ecosystems: Describe how autotrophs, photoautotrophs, and heterotrophs obtain nutrients"},
    {'id': 8957, 'description': "Scientific Method: Design and conduct complex experiments to test hypotheses using appropriate techniques and equipment"},
    {'id': 8958, 'description': "Public Speaking: Manage anxiety during public presentations"},
    {'id': 8953, 'description': "Creativity: Consider input and constructive feedback when creating or refining work"},
    {'id': 8999, 'description': "Scientific Method: Analyze different kinds of claims and evidence from a scientific point of view"},
    {'id': 8982, 'description': "Ecosystems: Diagram the water, carbon, nitrogen, and phosphorus cycles"},
    {'id': 8980, 'description': "Scientific Method: Collect, represent, evaluate, and analyze experimental data to draw evidence-based conclusions"},
    {'id': 8751, 'description': "Cells: Explain differences between plant, animal, and bacteria cells, describing differences and similarities in their parts and corresponding functions"},
    {'id': 8755, 'description': "Aesthetics: Describe specific features of a given work of art"},
    {'id': 8748, 'description': "Empathy: Experience others directly without prejudgment or prejudice, considering their perspective and point of view in earnest"},
    {'id': 8744, 'description': "Chemical Reactions: Explain how chemical properties of abundant elements and molecules on Earth result in macroscopic, observable physical properties"},
    {'id': 8736, 'description': "Reading: Analyze connections among a range of texts across literature, history, philosophy, and science"},
    {'id': 8731, 'description': "Reading: Summarize the main ideas in college-level texts from a variety of disciplines"},
    {'id': 8690, 'description': "Creativity: Create original expressions of emotion, experience, and thought"},
    {'id': 8686, 'description': "Earth: Predict the consequences of future changes to the Earth’s biome, landforms, bodies of water, climate, and continental plates"},
    {'id': 8683, 'description': "Reasoning: Form judgments, beliefs, and ideas based on sound reasoning and be able to persuasively present that reasoning"},
    {'id': 8678, 'description': "Atoms: Use atomic theory to describe properties of matter including density, mass, charge, and chemical composition"},
    {'id': 8671, 'description': "Writing: Write at a college level in a range of styles including academic argument, research essay, textual analysis, lab report, and technical writing"},
    {'id': 8665, 'description': "Reasoning: Form judgments, beliefs, and ideas based on sound reasoning and be able to persuasively present that reasoning"},
    {'id': 8819, 'description': "Metacognition: Critique one's own performance and work, identifying strengths and weaknesses"},
    {'id': 8814, 'description': "Cells: Explain the role of cell specialization in the development and maintenance of complex organisms"},
    {'id': 8811, 'description': "Discussion: Engage in and contribute to conversations on complex topics"},
    {'id': 8808, 'description': "Chemical Reactions: Explain how the periodic table is organized according to the properties of elements"},
    {'id': 8800, 'description': "Discussion: Engage in and contribute to conversations on complex topics"},
    {'id': 8924, 'description': "Chemical Reactions: Describe common chemical reactions including synthesis, decomposition, single displacement, double displacement, and combustion"},
    {'id': 8926, 'description': "Public Speaking: Utilize a range of presentation and performance tactics includiing dramatic pause, humor, varying cadence, and audience engagement"},
    {'id': 8917, 'description': "Empathy: Experience others directly without prejudgment or prejudice, considering their perspective and point of view in earnest"},
    {'id': 8875, 'description': "Ecosystems: Analyze the dynamics of a given ecosystem, explaining the complex web of dependencies between organisms and their environment"},
    {'id': 8872, 'description': "Discussion: Synthesize multiple perspectives and discussion points in one's own words"},
    {'id': 8869, 'description': "Chemical Reactions: Use the periodic table to describe and predict the behavior of an element"},
    {'id': 8863, 'description': "Public Speaking: Utilize a range of styles and strategies including storytelling, anecdote, argument, and exposition to achieve a self-identified goal"},
    {'id': 8858, 'description': "Public Speaking: Design and deliver clear and compelling presentations that resonate with their intended audiences"},
    {'id': 8880, 'description': "System Dynamics: Analyze global-scale problems from a systems perspective, identifying the complex causal and structural relationships that create them"},
    {'id': 8930, 'description': "Sustainability: Analyze the social, technological, economic, environmental, and political factors that impact sustainable practices and solutions"},
    {'id': 8914, 'description': "Reading: Summarize the main ideas in college-level texts from a variety of disciplines"},
    {'id': 8820, 'description': "Global Mindset: Demonstrate knowledge of and sensitivity to complex global economic, political, and social issues and their different manifestations in different communities"},
    {'id': 8794, 'description': "Public Speaking: Utilize a range of presentation and performance tactics includiing dramatic pause, humor, varying cadence, and audience engagement"},
    {'id': 8827, 'description': "Scientific Method: Collect, represent, evaluate, and analyze experimental data to draw evidence-based conclusions"},
    {'id': 8856, 'description': "Discussion: Engage in and contribute to conversations on complex topics"},
    {'id': 8663, 'description': "Planning: Define and set specific, measurable, attainable, relevant, and timely goals"},
    {'id': 8633, 'description': "Energy: Explain energy, differentiating between its forms and means of transfer"},
    {'id': 8698, 'description': "Energy: Apply common energy formulas including those for work, force, power, kinetic, elastic, and potential to solve problems"},
    {'id': 8691, 'description': "Research: Leverage search engines, databases, libraries, and archives independently and as appropriate to access information that answers a wide range of given and self-identified questions"},
    {'id': 8729, 'description': "Writing: Utilize a range of written narrative structures to tell real or imagined events"},
    {'id': 8756, 'description': "National History: Interpret past events in their historical, cultural, social, and political contexts"},
    {'id': 8763, 'description': "Chemical Reactions: Describe common chemical reactions including synthesis, decomposition, single displacement, double displacement, and combustion"},
    {'id': 9336, 'description': "Planning: Define and set specific, measurable, attainable, relevant, and timely goals"},
    {'id': 9337, 'description': "Writing: Utilize a range of written narrative structures to tell real or imagined events"},
    {'id': 9338, 'description': "Public Speaking: Utilize a range of presentation and performance tactics includiing dramatic pause, humor, varying cadence, and audience engagement"},
    {'id': 9339, 'description': "Discussion: Engage in and contribute to conversations on complex topics"},
    {'id': 9340, 'description': "Reading: Summarize the main ideas in college-level texts from a variety of disciplines"},
]


##################################################### 
# 
# App Routes
#
##################################################### 

@app.route("/")
def main():
    return 'Choose a route.'

@app.route("/update_proficiencies/<campus>/")
def update_proficiencies(campus):
    # define school id
    if campus == 'sp':
        school_id = 3

    # get all final proficiencies (Canvas Extension DB)
    proficiencies = asyncio.run(get_all_proficiencies(school_id))
    
    # get all outcomes links (Canvas Extension DB)
    outcomes_links = asyncio.run(get_all_outcomes_links(school_id))

    # get all subjects (Canvas Extension DB)
    subjects = asyncio.run(get_all_subjects(school_id))

    # get all proficiency values (Canvas Extension DB)
    proficiency_values = asyncio.run(get_proficiency_values())

    # add proficiency as expected by Veracross
    for p in proficiencies:
        for v in proficiency_values:
            if p['proficiencyValueID'] == v['proficiencyValueID']:
                proficiency_desc_words = v['proficiencyDesc'].split(' ')
                veracrossProf = ''
                for w in proficiency_desc_words:
                    veracrossProf = veracrossProf + w[0]
                p['veracrossProficiency'] = veracrossProf

    # add veracrossSubjectID to each proficiency
    for p in proficiencies:
        for l in outcomes_links:
            if p['outcomeLinkID'] == l['outcomeLinkID']:
                p['outcomeID'] = l['outcomeID']
                p['courseID'] = l['courseID']
                p['subjectID'] = l['subjectID']

    for p in proficiencies:
        for s in subjects:
            if p['subjectID'] == s['subjectID']:
                p['subjectName'] = s['subjectName']
                p['gradeLevel'] = s['gradeLevel']
                p['veracrossSubjectID'] = s['veracrossSubjectID']
                p['academicYear'] = s['academicYear']

    # get all outcomes (Canvas Extension DB)
    outcomes_ids = []
    for p in proficiencies:
        if p['outcomeID'] not in outcomes_ids:
            outcomes_ids.append(p['outcomeID'])

    outcomes = asyncio.run(get_outcomes(campus,outcomes_ids))

    # add outcomes data to the proficiencies list
    for p in proficiencies:
        for o in outcomes:
            if p['outcomeID'] == o['outcomeID']:
                p['outcomeTitle'] = o['outcomeTitle']
                p['outcomeDescription'] = o['outcomeDescription'].strip()

    # add Veracross outcome ID
    for p in proficiencies:
        for o in vx_outcomes_data:
            if p['outcomeDescription'] == o['description'].split(":",1)[1].strip():
                if 'veracrossOutcomeID' not in p:
                    p['veracrossOutcomeID'] = []
                if o['id'] not in p['veracrossOutcomeID']:
                    p['veracrossOutcomeID'].append(o['id'])

    # get Veracross classes list
    classes = asyncio.run(get_classes(campus))
    if classes:
        token = classes['token']

    # identify the assessed classes
    subjects_assessed =[]
    for p in proficiencies:
        if p['veracrossSubjectID'] not in subjects_assessed:
            subjects_assessed.append(p['veracrossSubjectID'])

    classes_assessed = []
    for s in subjects_assessed:
        for c in classes['data']:
            if s == c['course']['id']:
                if c['id'] not in classes_assessed:
                    classes_assessed.append(c['id'])
                    # associate each proficiency to one (or more) identified classes 
                    for p in proficiencies:
                        if p['veracrossSubjectID'] == c['course']['id']:
                            if 'veracrossClassID' not in p:
                                p['veracrossClassID'] = []
                            if c['course']['id'] not in p['veracrossClassID']:
                                p['veracrossClassID'].append(c['id'])

    # get Canvas users
    students = asyncio.run(get_all_students(campus))

    # add student's Veracross ID to each proficiency
    for p in proficiencies:
        for s in students:
            if p['userID'] == s['id']:
                p['veracrossUserID'] = s['sisID']
                p['userName'] = s['name']

    # get Veracross Qualitative Grades for each class assessed
    grades = asyncio.run(get_qualitative_grades(classes_assessed,'academics/qualitative_grades',campus,token))
    if grades:
        token = grades['token']

    # get Veracross Grading Periods and define the current one
    grading_periods = asyncio.run(get_grading_periods(campus,token))
    if grading_periods:
        token = grading_periods['token']
    
    for g in grading_periods['data']:
        start_date = datetime.strptime(g['start_date'][:10], '%Y-%m-%d')
        end_date = datetime.strptime(g['end_date'][:10], '%Y-%m-%d')
        today = datetime.now()

        if today >= start_date and today <= end_date: # valid date
            if g['group']['description'] == 'SS Semesters':
                if g['abbreviation'] == 'S1' or g['abbreviation'] == 'S2':
                    current_grading_period = g['id']

    # add Veracross Grade ID to each proficiency
    for p in proficiencies:
        for g in grades['data']:
            if p['veracrossUserID'] == g['student']['id'] and g['class']['id'] in p['veracrossClassID'] and g['rubric_criteria']['id'] in p['veracrossOutcomeID']:
                if g['grading_period']['id'] == current_grading_period:
                    if 'veracrossGradeID' not in p:
                        p['veracrossGradeID'] = g['id']
                    else:
                        return 'More than 1 Veracross Grade ID was found for the same final proficiency!'
    
    return 'OK!'

@app.route("/update_letter_grades/<campus>/")
def update_letter_grades(campus):
    # define school id
    if campus == 'sp':
        school_id = 3

    # get all final proficiencies (Canvas Extension DB)
    letter_grades = asyncio.run(get_all_letter_grades(school_id))

    # get all subjects (Canvas Extension DB)
    subjects = asyncio.run(get_all_subjects(school_id))

    # get all letter grade values (Canvas Extension DB)
    letter_grade_values = asyncio.run(get_letter_grade_values())

    # add letter grades as expected by Veracross
    for l in letter_grades:
        for v in letter_grade_values:
            if l['letterGradeValueID'] == v['letterGradeValueID']:
                l['veracrossLetterGrade'] = v['letterGradeDesc'].replace('Warning', 'NR')

    # add veracrossSubjectID to each proficiency
    for l in letter_grades:
        for s in subjects:
            if l['subjectID'] == s['subjectID']:
                l['subjectName'] = s['subjectName']
                l['gradeLevel'] = s['gradeLevel']
                l['veracrossSubjectID'] = s['veracrossSubjectID']
                l['academicYear'] = s['academicYear']

    # get Veracross classes list
    classes = asyncio.run(get_classes(campus))
    if classes:
        token = classes['token']

    # identify the assessed classes
    subjects_assessed =[]
    for l in letter_grades:
        if l['veracrossSubjectID'] not in subjects_assessed:
            subjects_assessed.append(l['veracrossSubjectID'])

    classes_assessed = []
    for s in subjects_assessed:
        for c in classes['data']:
            if s == c['course']['id']:
                if c['id'] not in classes_assessed:
                    classes_assessed.append(c['id'])
                    # associate each letter grade to one (or more) identified classes 
                    for l in letter_grades:
                        if l['veracrossSubjectID'] == c['course']['id']:
                            if 'veracrossClassID' not in l:
                                l['veracrossClassID'] = []
                            if c['course']['id'] not in l['veracrossClassID']:
                                l['veracrossClassID'].append(c['id'])

    # get Canvas users
    students = asyncio.run(get_all_students(campus))

    # add student's Veracross ID to each proficiency
    for l in letter_grades:
        for s in students:
            if l['userID'] == s['id']:
                l['veracrossUserID'] = s['sisID']
                l['userName'] = s['name']

    # get Veracross letter grades for each class assessed
    grades = asyncio.run(get_letter_grades(classes_assessed,'academics/numeric_grades',campus,token))
    if grades:
        token = grades['token']

    # get Veracross Grading Periods and define the current one
    grading_periods = asyncio.run(get_grading_periods(campus,token))
    if grading_periods:
        token = grading_periods['token']
    
    for g in grading_periods['data']:
        start_date = datetime.strptime(g['start_date'][:10], '%Y-%m-%d')
        end_date = datetime.strptime(g['end_date'][:10], '%Y-%m-%d')
        today = datetime.now()

        if today >= start_date and today <= end_date: # valid date
            if g['group']['description'] == 'SS Semesters':
                if g['abbreviation'] == 'S1' or g['abbreviation'] == 'S2':
                    current_grading_period = g['id']

    # add Veracross Grade ID to each proficiency
    for l in letter_grades:
        for g in grades['data']:
            if l['veracrossUserID'] == g['student']['id'] and g['class']['id'] in l['veracrossClassID']:
                if g['grading_period']['id'] == current_grading_period:
                    if 'veracrossGradeID' not in l:
                        l['veracrossGradeID'] = g['id']
                    else:
                        return 'More than 1 Veracross Grade ID was found for the same letter grade!'

    print(letter_grades[0],flush=True)
    
    return 'OK!'

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=9000, debug=True)