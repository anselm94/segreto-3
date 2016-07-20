from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from segreto.idea import IdeaCollection, Idea


class IdeaScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.idea_collection = IdeaCollection()
        self.register_event_type('on_quit_app')

    def remove_idea(self, instance):
        self.idea_collection.remove_idea(instance.idea)
        self.ids['idea_container'].ids['container'].remove_widget(instance)

    def set_idea_collection(self, idea_collection):
        self.idea_collection = idea_collection
        for idea in self.idea_collection.ideas:
            self.add_ideawidget(idea)

    def new_idea(self):
        self.add_ideawidget(self.idea_collection.new_idea())

    def add_ideawidget(self, idea):
        ideawidget = IdeaWidget()
        ideawidget.idea = idea
        ideawidget.bind(on_delete = self.remove_idea)
        ideawidget.bind(on_idea_changed = self.modify_idea)
        self.ids['idea_container'].ids['container'].add_widget(ideawidget)

    def modify_idea(self, instance):
        self.idea_collection.modify_idea(instance.idea)

    def pre_quit_exec(self):
        for child in self.ids['idea_container'].ids['container'].children:
            child.edit_mode = False
        self.dispatch('on_quit_app')

    def on_quit_app(self):
        pass


class TopBar(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_add_ideawidget')
        self.register_event_type('on_quit_pressed')

    def on_add_ideawidget(self):
        pass

    def on_quit_pressed(self):
        pass


class IdeaTitleBar(BoxLayout):

    idea_no = StringProperty()
    stamp = StringProperty()
    but_edit = ObjectProperty(None)
    but_del = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_del_pressed')
        self.register_event_type('on_edit_pressed')

    def on_idea_no(self, instance, value):
        self.ids['lbl_idea_no'].text = value

    def on_stamp(self,instance, value):
        self.ids['lbl_date'].text = value

    def on_del_pressed(self):
        pass

    def on_edit_pressed(self):
        pass

class IdeaWidget(StackLayout):

    edit_mode = BooleanProperty(True)
    idea = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_delete')
        self.register_event_type('on_idea_changed')

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode

    def on_edit_mode(self, instance, value):
        if value:
            self.ids['inp_idea'].disabled = False
            self.ids['title_bar'].but_edit.background_normal = 'data/images/src/but_edit_down.png'
        else:
            self.ids['inp_idea'].disabled = True
            self.ids['title_bar'].but_edit.background_normal = 'data/images/src/but_edit.png'
            self.idea.set_mesg(self.ids['inp_idea'].text)
            self.ids['title_bar'].ids['lbl_date'].text = self.idea.time
            self.dispatch('on_idea_changed')

    def on_delete(self):
        return self

    def on_idea_changed(self):
        return self

    def on_idea(self, instance, value):
        self.ids['title_bar'].ids['lbl_idea_no'].text = '#' + str(self.idea.num)
        self.ids['title_bar'].ids['lbl_date'].text = self.idea.time
        self.ids['inp_idea'].text = self.idea.get_mesg()
        if self.ids['inp_idea'].text == '':
            self.edit_mode = True
        else:
            self.edit_mode = False
