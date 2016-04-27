import sqlite3
import nltk
import os
import traceback
import logging

logger = logging.getLogger(__name__)

class RecipeDB(object):
    def __init__(self, dbname):
        self.db = os.path.join(os.getcwd(), dbname)
        self.createTables()

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #fh.setFormatter(formatter)
        ch.setFormatter(formatter)


        self.logger = logging.getLogger('recipe_sql.RecipeDB')
        self.logger.addHandler(ch)



    def createTables(self):
        con = sqlite3.connect(self.db)

#######   TABLES
        # drop table if exists - to remove table
        con.execute('create table if not exists ingredient \
            (ingredient_id integer primary key autoincrement, \
            ingredient_name text unique not null, \
            ingredient_brand text, \
            ingredient_description text) ')	
        

        # drop table if exists - to remove table
        con.execute('create table if not exists recipe \
            (recipe_id integer primary key autoincrement, \
            recipe_name text unique not null) ')


        # drop table if exists - to remove table
        con.execute('create table if not exists ingredient_calorie \
            (ingredient_id integer references ingredient(ingredient_id), \
            calorie_count integer, measuring_unit text) ')


        # drop table if exists - to remove table
        con.execute('create table if not exists \
        	recipe_ingredient_quantity \
            (recipe_id integer primary key, \
            ingredient_id integer, \
            ingredient_quantity real, \
            ingredient_unit text) ')

        # drop table if exists - to remove table
        con.execute('create table if not exists \
        	recipe_step \
            (recipe_id references recipe(recipe_id), \
            step_id integer primary_key, \
            step_description text) ')

        # drop table if exists - to remove table
        con.execute('create table if not exists \
        	recipe_step_ingredient \
            ( rsi_id integer primary key autoincrement, \
            recipe_id references recipe(recipe_id), \
            step_id references recipe_step(step_id), \
            ingredient_id references ingredient(ingredient_id), \
            r_ingredient_quantity integer, \
            r_ingredient_unit text) ')


        # drop table if exists - to remove table
        con.execute('create table if not exists producer \
            (producer_id integer primary key autoincrement, \
            producer name text unique, \
            producer_description text) ')	


    def connect(self):
    	con = sqlite3.connect(self.db)
        cur = con.cursor()
        return (con, cur)
    
    
    def initialPopulate(self):
        con = sqlite3.connect(self.db)
        # REMOVE LATER
        recipes = [
            ( "Royal Russian Easter pashka",),
            ( "Breakfast Lavash with Eggs",)
            ]

        ingredients = [
            (1, "Lifeway cottage cheese", "Lifeway", 'low fat'),
            (2, "TJ unrefined organic sugar", 'Trader Joes', 'unrefined')
            ]

        recipe_ingredient_quantities = [
            (1, 1, '500', 'g'),
            (1, 2, '100', 'g')
            ]


        with con:
            con.executemany('insert or ignore into ingredient( \
            	ingredient_id, ingredient_name, \
            	ingredient_brand, ingredient_description) \
                values (?, ?, ?, ?)', ingredients)

        print 'INGEREDIENT TABLE PRINTOUT'
        for row in con.execute("select * from ingredient"):
            print row	    

        with con:
            con.executemany('insert or ignore into recipe(recipe_name )\
            	values (?)', recipes)
                
        with con:
            con.executemany('insert or ignore into recipe_ingredient_quantity(recipe_id, \
            	ingredient_id, ingredient_quantity, ingredient_unit) \
                values (?, ?, ?, ?)', recipe_ingredient_quantities)            

        print 'RECIPE TABLE PRINTOUT'
        for row in con.execute("select recipe_id, recipe_name from recipe"):
            print row	


        print 'RECIPE_INGREDIENT_QUANTITY PRINTOUT'
        for row in con.execute("select * from recipe_ingredient_quantity"):
            print row

        con.commit()   
        con.close() 	   




#############################################################
# INGREDIENT 
########################################

    def insertIngredient(self, ingredient, brand='', description=''):
    	'''
    	Insert into ingredient table
    	@ingredient: text
    	@ brand: text
    	@ description: text
    	'''
        ing_id = None

        ingredients = [ingredient, brand, description]

        con, cur = self.connect()
        with con:
            con.execute('insert or ignore into ingredient( \
            	ingredient_name, \
            	ingredient_brand, ingredient_description) \
                values (?, ?, ?)', ingredients)
            cur.execute('select ingredient_id from ingredient' + \
        	' where ingredient_name="' +  str(ingredient)+'"') 

            v = cur.fetchone()
            
            if v:
            	ing_id = v[0]
        return ing_id 


    def getIngredientID(self, name):
        r_id = None

        con, cur = self.connect()
        cur.execute('select ingredient_id from ingredient ' + \
        	' where ingredient_name="' +  str(name)+'"') 
        	
        v = cur.fetchone() 
        self.logger.debug( 'Ingredient id is ' + str(v)     )  
        if v:
            r_id = v[0]            
        return r_id	  

    def getIngredientName(self, iid):
        name = None
        (con, cur) = self.connect()

        cur.execute('SELECT ingredient_name FROM ingredient ' + \
        	' WHERE ingredient_id="' +  str(iid)+'"') 
        	
        v = cur.fetchone() 
        print 'Ingredient id is ' + str(v)       
        if v:
            name = v[0]            
        return name	   


    def removeIngredient(self, ingredient):
        con, cur = self.connect()
        cur.execute('select ' + column_name + ' from ' + \
        	table_name + ' where ' + ingredient_name + '=' \
        	+ ingredient)
        con.close()	 



    def insertIngredientIntoRecipe(self, recipe, ingredient, 
    	    amount, unit= 'oz', step = ''):
    	'''
    	Insert into ingredient table
    	@ingredient: text
    	@ brand: text
    	@ description: text
    	'''

    	recipe_id = self._getRecipeID(recipe)
    	step_id = self.getStepID(recipe, step)
        ingredient_id = self.getIngredientID(ingredient)
        ingredients = [recipe_id, step_id, ingredient_id, amount, unit]
        con, cur = self.connect()
        with con:
            cur.execute('insert or ignore into recipe_step_ingredient( \
            	recipe_id, \
            	step_id, \
            	ingredient_id, \
            	r_ingredient_unit, \
            	r_ingredient_quantity) \
                values (?, ?, ?, ?, ?)', (ingredients))  
            cur.execute('select * from recipe_step_ingredient where \
            ingredient_id=' + str(ingredient_id))
            v = cur.fetchone()
            print v                    



    def insertIngredientIntoRecipeOLD(self, recipe, step, ingredient, 
    	    amount, unit):
    	'''
    	Insert into ingredient table
    	@ingredient: text
    	@ brand: text
    	@ description: text
    	'''

    	recipe_id = self._getRecipeID(recipe)
    	step_id = self.getStepID(recipe, step)
        
        
        con, cur = self.connect()
        with con:
            ingredient_id = self.getIngredientID(ingredient)
            if not ingredient_id:
                cur.execute('insert or ignore into ingredient( \
                ingredient_name, \
                brand, \
                description) \
                values (?, ?, ?)', (ingredient, None, None))
            ingredient_id = self.getIngredientID(ingredient)
            ingredients = [recipe_id, step_id, ingredient_id, amount, unit]	
            cur.execute('insert or ignore into recipe_step_ingredient( \
            	recipe_id, \
            	step_id, \
            	ingredient_id, \
            	r_ingredient_unit, \
            	r_ingredient_quantity) \
                values (?, ?, ?, ?, ?)', (ingredients))  
            cur.execute('select * from recipe_step_ingredient where \
            ingredient_id=' + str(ingredient_id))
            v = cur.fetchone()
            print v                                   	

#########################################################
# COMMON GETTERS
#########################################################
    def getRecordID(self, table, colname, name):
        record = None
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        with con:
        	cur.execute('select ' + colname + ' from ' + table + \
        	' where ' + colname + '_name="' +  str(name)+'"') 

        return record    

    def getRecord(self, table_name, column_one, column_two, value):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        with con:
            cur.execute('select ' + column_one + ' from ' + table_name + \
            ' where ' + column_two + '="' +  str(value)+'"') 
        v = cur.fetchall()
        print v
        con.close()
        return v	     
                 
    def getID(self, table, colname, name):
    	''' 
    	Does not work in all cases, but maybe later
        Example: getID('ingredient', 'ingredient', 'butter')

    	'''
        
        r_id = None
        #con = sqlite3.connect(self.db)
        #cur = con.cursor()
        con, cur = self.connect()
        cur.execute('select ' + colname + '_id from ' + table + \
        	' where ' + colname + '_name="' +  str(name)+'"') 
        	
        v = cur.fetchone()
        print 'From getID() function, the query returned ' + str(v)
        if v:
            r_id = v[0]
            
        return r_id	     
            

    def updateRecord(self, table, cols_vals_to_change, colname, record):
        '''
        UPDATE table_name
        SET column1=value1,column2=value2,...
        WHERE some_column=some_value;


        '''
        if not isinstance(cols_vals_to_change, dict):
        	raise Exception('first argument should be \
        		dictionary column:value to change')
        new_string = ''
        new_list = []
        for c, v in cols_vals_to_change.iteritems():
        
        	new_string += c + '=? '
        	new_list.append(v)
        new_list.append(record)	
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        with con:
          cur.execute('UPDATE ' + table + ' SET ' + new_string + \
            	'WHERE ' + str(colname) + "=?", (new_list))
        v = cur.fetchall()
        if v:
        	ret = v[0]
           	print ret
            

    def getTables(self, table = '*'):
    	'''
    	return all tables from database
    	'''
    	con = sqlite3.connect(self.db)
    	cur = con.cursor()
    	cur.execute('select name from sqlite_master where  type="table"')

    	tables = cur.fetchall()
    	
    	con.close()
    	return tables    


    def getColumnNames(self, table):
    	# Connecting to the database file
        conn = sqlite3.connect(self.db)
        c = conn.cursor()

        # Retrieve column information
        # Every column will be represented by a tuple with the following attributes:
        # (id, name, type, notnull, default_value, primary_key)
        c.execute('PRAGMA TABLE_INFO({})'.format(table_name))

        # collect names in a list
        names = [tup[1] for tup in c.fetchall()]
        print(names)
        # e.g., ['id', 'date', 'time', 'date_time']

        # Closing the connection to the database file
        conn.close()
        return names	
    


###################################
# STEP
#####################################

    def insertStep(self, recipe_name, description):
    	'''
    	Insert into ingredient table
    	@step_description: text
    	@ recipe_name: text
    	
    	'''
        step_id = None
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        recipe_id = self.getRecipe(recipe_name)
        #print 'From insertStep function, recipe id for this step is ' + str(recipe_id)
        steps = [recipe_id, description]
        with con:
            con.execute('insert or ignore into recipe_step( \
            	recipe_id, \
            	step_description) \
                values (?, ?)', steps)
            con.execute('select step_id from recipe_step' + \
        	' where recipe_id="' +  str(recipe_id)+'"' \
        	' and step_description="' + str(description) + '"')
        	
            v = cur.fetchone()
            if v:
            	step_id = v[0]
        return step_id    	


    def getStepID(self, recipe_id, step_description):
        step_id = None
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        with con:

            con.execute('select step_id from recipe_step' + \
        	' where recipe_id="' +  str(recipe_id)+'"' \
        	' and step_description="' + str(step_description) + '"')
        	
            v = cur.fetchone()
            if v:
            	step_id = v[0]
        return step_id


    def updateStep(self, stepname):
        self.updateRecord('step', )    

##################################################
# RECIPE
###################################################
    
    def _getRecipeID(self, name):
    	'''
    	@ input: recipe name
    	@ output: recipe ID
    	'''
        
        recipe_id = None
        con, cur = self.connect()
        with con:
            cur.execute('select recipe_id from recipe' + \
        	' where recipe_name="' +  str(name)+'"')        	
            v = cur.fetchone()
            if v:
            	recipe_id = v[0]
            
        return recipe_id	     
 
  

  

    def getRecipe(self, name):
    	'''
    	Insert into recipe table    	
    	@ recipe_name: text    	
    	'''   	       
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        with con:
            con.execute('insert or ignore into recipe \
            	    (recipe_name) values (?);', (name,))
        recipe_id = self._getRecipeID(name)        
        return recipe_id  


    def insertRecipe(self, name):
    	return self.getRecipe(name)


    def getRecipeName(self, rid):
        '''
        Return recipe name
        '''	
        con, cur = self.connect()
        with con:
            cur.execute('select recipe_name from recipe \
            	where recipe_id="' + str(rid) + '"')
            name = cur.fetchone()
            if name:
            	name = name[0]
        return name 

    def getRecipeIngredients(self, name):
        ingredients = []
        con, cur = self.connect()
        with con:
            cur.execute('select recipe_id from recipe \
            	where recipe_name="' + name + '"')
            steps = cur.fetchone()[0]
            cur.execute('select recipe_ingredient quantity from \
            	recipe_step_ingredient' + \
        	    ' where recipe_id="' +  str(rid)+'"')        	
            steps = cur.fetchall()
        #recipe_step_ingredient
        return ingredients 


    def getRecipeSteps(self, name):
        steps = []
        con, cur = self.connect()
        with con:
            cur.execute('select recipe_id from recipe \
                where recipe_name="' + name + '"')
            v = cur.fetchall()
            rid = v[0]
            cur.execute('select step_description from recipe_step' + \
        	' where recipe_id="' +  str(rid)+'"')        	
            steps = cur.fetchall()


      
        return steps       







    
    

class Recipe:
    '''
    Just holds itemised
    recipe information
    wraps the database

    '''
    def __init__(self, name):
        self.name = name
        self.ingredients = {}
        
        self.steps = []   
        self.time = 0
        self.calories = 0


    def printRecipe(self, recipe_name):
        '''
        print formatted recipe
        '''   
        pass

    def verify(self):
    	'''
    	should have 
    	all values
    	'''
    	assert(self.name)
    	assert(self.calories)
    	assert(self.steps)
    	assert(self.time)
    	assert(self.ingredients)

    def calculateCalories(self):
    	'''
    	summarise calories from the 
    	recipe database
    	'''
        calories = 0
        ingredients = self.queryData()
        calories = 0
        for i in ingredients:
        	calories += ingredients[i]
        return calories	



    def queryData(self):
    	'''
    	Ingredients and amount
    	from recipe database or other
    	source, to count calories
    	'''
    	ingredients = {}
        return ingredients           

    def addRecipe(self):
    	pass



def main():
    r = RecipeDB('recipes.sqlite')     
    r.getRecord( 'recipe', 'recipe_name', 'eggLavash')
    
    #print 'DB tables:'
    #print(r.getTables())


    r.insertIngredient('Kerrygold unsalted butter', 'kerrygold', 'unsalted')
    recipe_id = r.getRecipe('Grandma Tamara pelmeni')
    r.insertStep('Grandma Tamara pelmeni', 
    	    'Mix WWWater, egg, and flour to get the dough')





if __name__ == '__main__':
	main()



