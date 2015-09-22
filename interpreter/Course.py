
class Course ():
    coursename = ""
    groups = []
    
    def get_coursename(self):
        return self.__coursename
    
    def set_coursename(self, value):
        self.__coursename = value
    
    def get_groups(self):
        return self.groups
    def setGroupList(self,group):
        for i in self.groups :
            if group.get_groupname() == i.get_groupname() :
                print "The group already exists in the accountobject"
            else :
                self.groups.append(group)
        
        
