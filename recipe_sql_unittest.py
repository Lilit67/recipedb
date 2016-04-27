import recipe_sql
import unittest
import sqlite3
import sys
import logging


logger = logging.getLogger(__name__)




class TestRecipeDB(unittest.TestCase):
    #def __init__(self):
    	#TestRecipeDB.super.__init__(self)
    @classmethod
    def setUpClass(cls):    	
        ch = logging.StreamHandler()
        #ch.setLevel(logging.INFO)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #fh.setFormatter(formatter)
        ch.setFormatter(formatter)


        cls.logger = logging.getLogger('recipe_sql_unittest.TestRecipeDB')
        cls.logger.addHandler(ch)
        cls.db = recipe_sql.RecipeDB('testrecipe.sqlite')
        #cls.con = sqlite3.connect('testrecipe.sqlite')
        #cls.con.row_factory = sqlite3.Row

    @classmethod
    def tearDownClass(cls):
    	#cls.con.close()
    	pass

    def testAddNewRecipe(self):
        rec_id = TestRecipeDB.db.getRecipe('TestRecipe')
        self.logger.debug( 
        	': recipe id is ' + str(rec_id))
        rec_id = TestRecipeDB.db.getRecipe('TESTRECIPE')
        self.logger.debug(rec_id)	


    def testAddNewIngredient(self):
    	'''
    	just add ingredient
    	not connected to recipe
    	'''
    	ingredient_name = 'TJ unsalted butter'
    	brand = 'Trader Joes'


    	ing_id = TestRecipeDB.db.insertIngredient(ingredient_name, 
    		brand, 'unsalted, not very fatty')
    	print ('Ingredient id is ' + str(ing_id))
    	self.assertEqual(ing_id, 1, 'Incorrect ingredient id ' + str(ing_id))

    	r_id =  TestRecipeDB.db.getID('ingredient', 'ingredient', 'TJ unsalted butter')
        self.assertEqual(r_id, ing_id, 
        	'ID-s are not equal for record ' +  ingredient_name)

    
    def testInsertIngredientIntoRecipe(self):
    	recipe = 'TestRecipe'
    	step = 'FirstTestStep'
    	ingredient = 'FirstTestIngredient'
    	amount = 8
    	unit = 'kg'

        recipe_id = TestRecipeDB.db.insertRecipe(recipe)
        print recipe_id


        ingredient_id = TestRecipeDB.db.insertIngredient(ingredient, 'TestBrand')
    	TestRecipeDB.db.insertIngredientIntoRecipe( recipe_id, step, ingredient, 
    	    amount, unit)
    	
    	   	
    	this_function_name = sys._getframe().f_code.co_name
        print (this_function_name + ': ingredient id is ' + str(ingredient_id))
        
######################################
# RECIPE_STEP

    def testAddNewStep(self):
    	'''
        
    	'''
    	recipe = ''
        teststep = 'mix eggs with sugar. Beat during 5 minutes until fluffy'


    def testUpdateStep(self):
        pass



    def testGetStep(self):
        pass         


    def testAddNewColumnToIngredient(self):
        pass	

    
    def testUpdateIngredient(self):
    	'''
        create new ingredient 
        then update and asseert it
    	'''
    	ingredient_name = 'TJ salted butter'
    	brand = 'Trader Joes'
        to_change = {'ingredient_description': 'Do not use for sweet baked goods'}

    	ing_id = TestRecipeDB.db.insertIngredient(ingredient_name, 
    		brand, 'salted, not very fatty')
    	#print ('Ingredient id is ' + str(ing_id))
        TestRecipeDB.db.updateRecord( 'ingredient', 
        	to_change, 'ingredient_id', ing_id)
        
        new_record = TestRecipeDB.db.getRecord('ingredient', '*', 
        	'ingredient_id', ing_id)
        

        new_record = TestRecipeDB.db.getRecord('ingredient', 'ingredient_brand',
        	'ingredient_id', ing_id)
        





    
if __name__ == '__main__':
    unittest.main()
