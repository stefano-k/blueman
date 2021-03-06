# Copyright (C) 2008 Valmantas Paliksa <walmis at balticum-tv dot lt>
# Copyright (C) 2008 Tadas Dailyda <tadas at dailyda dot com>
#
# Licensed under the GNU General Public License Version 3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
import gtk


class GenericList(gtk.TreeView):

	def __init__(self, data):
		gtk.TreeView.__init__(self)
		self.selection = self.get_selection()
		self._load(data)
		
		

	def _load(self, data):
		
		self.ids = {}
		self.columns = {}
		

		types = []
		for i in range(len(data)):
			types.append(data[i][1])
			
		types = tuple(types)
		
		self.liststore = gtk.ListStore(*types)
		self.set_model(self.liststore)
		column = None
		for i in range(len(data)):

			self.ids[data[i][0]] = i
			
			
			if len(data[i]) == 5 or len(data[i]) == 6:

				column = gtk.TreeViewColumn(data[i][4])
				
				column.pack_start(data[i][2])
				column.set_attributes(data[i][2], **data[i][3])				
				
				
				if len(data[i]) == 6:
					column.set_properties(**data[i][5])
				
				self.columns[data[i][0]] = column
				self.append_column(column)
				

    
	def selected(self):
		(model, iter) = self.selection.get_selected()
               
               	return iter

                	
    
    	def delete(self, id):
		if type(id) == gtk.TreeIter:
			iter = id
		else:
			iter = self.get_iter(id)
    		
    		if iter == None:
    			return False
    		if self.liststore.iter_is_valid(iter):
    			self.liststore.remove(iter)
    			return True
    		else:
    			return False
    			
    	
    	def _add(self, **columns):
    		ids_len = len(self.ids)
    		cols_len = len(columns)
    		
		items = {}
    		for k, v in self.ids.iteritems():
    			items[v] = None
	
 		
    		for k, v in columns.iteritems():
    			if k in self.ids:
    				items[self.ids[k]] = v
    			else:
    				raise Exception, "Invalid key %s" % k
    				
		return items.values()
		
	def append(self, **columns):
		vals = self._add(**columns)
		return self.liststore.append(vals)
	
	def prepend(self, **columns):
		vals = self._add(**columns)
		return self.liststore.prepend(vals)
    		
	def get_conditional(self, **cols):
   		ret = []
   		matches = 0
   		for i in range(len(self.liststore)):
   			row = self.get(i)
    			for k, v in cols.iteritems():
    				if row[k] == v:
    					matches += 1
    					
    			if matches == len(cols):
    				ret.append(i)
    				
    			matches = 0

    		return ret
    		
    		
    	def set(self, id, **cols):
		if type(id) == gtk.TreeIter:
			iter = id
		else:
			iter = self.get_iter(id)
		
		if iter != None:
	    		for k, v in cols.iteritems():
	    			self.liststore.set(iter, self.ids[k], v)
	    		return True
		else:
	    		return False

    	
    	
    	def get(self, id, *items):
		ret = {}

		if id != None:
			if type(id) == gtk.TreeIter:
				iter = id
			else:
				iter = self.get_iter(id)
			if len(items) == 0:
				for k, v in self.ids.iteritems():
					ret[k] = self.liststore.get(iter, v)[0]
			else:
				for i in range(len(items)):
					if items[i] in self.ids:
						ret[items[i]] = self.liststore.get(iter, self.ids[items[i]])[0]
		else:
			return False

	
		return ret

        	
  	
    	def get_iter(self, path):
        	if path == None:
        		return None
        	
        	try:
            		return self.liststore.get_iter(path)
        	except:
            		return None
            		
	def clear(self):
		self.liststore.clear()
		
	def compare(self, iter_a, iter_b):
		if iter_a != None and iter_b != None:
			return self.get_model().get_path(iter_a) == self.get_model().get_path(iter_b)
		else:
			return False

