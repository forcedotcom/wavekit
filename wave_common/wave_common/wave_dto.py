"""
Copyright (c) 2018, Salesforce.com, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of Salesforce.com nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import json
import inspect
from utils import Logger

logger = Logger.logger


########################################################################################################################
# serialization utils
########################################################################################################################
class ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_json") or hasattr(obj, "__dict__"):
            d = dict(
                (key, value)
                for key, value in inspect.getmembers(obj)
                if not key.startswith("__")
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )
            return self.default(d)
        return obj


class JSONSerializable(object):
    def __str__(self):
        return json.dumps(self.__dict__, cls=ObjectEncoder, indent=2, sort_keys=True)

    def __repr__(self):
        return json.dumps(self.__dict__, cls=ObjectEncoder, indent=2, sort_keys=True)

    def to_json(self):
        return json.dumps(self.__dict__, cls=ObjectEncoder)


########################################################################################################################
# lens
########################################################################################################################
class Lens(JSONSerializable):
    def __init__(self,
                 allowPreview=False,
                 assetSharingUrl='',
                 createdBy=None,
                 createdDate='',
                 dataset=None,
                 files=None,
                 filesUrl='',
                 folder=None,
                 id='',
                 label='',
                 lastAccessedDate='',
                 lastModifiedBy=None,
                 lastModifiedDate='',
                 name='',
                 permissions=None,
                 refreshDate='',
                 state=None,
                 type='',
                 url='',
                 visualizationType=''
                 ):
        if createdBy is None:
            createdBy = {}
        if dataset is None:
            dataset = {}
        if files is None:
            files = []
        if folder is None:
            folder = {}
        if lastModifiedBy is None:
            lastModifiedBy = {}
        if permissions is None:
            permissions = {}
        if state is None:
            state = {}

        self.allowPreview = allowPreview
        self.assetSharingUrl = assetSharingUrl
        self.createdBy = WaveUser.from_json(createdBy)
        self.createdDate = createdDate
        self.dataset = AssetReferenceRepresentation.from_json(dataset)
        self.files = [LensFile.from_json(file_item) for file_item in files]
        self.filesUrl = filesUrl
        self.folder = AssetReferenceRepresentation.from_json(folder)
        self.id = id
        self.label = label
        self.lastAccessedDate = lastAccessedDate
        self.lastModifiedBy = WaveUser.from_json(lastModifiedBy)
        self.lastModifiedDate = lastModifiedDate
        self.name = name
        self.permissions = Permissions.from_json(permissions)
        self.refreshDate = refreshDate
        self.state = LensState.from_json(state)
        self.type = type
        self.url = url
        self.visualizationType = visualizationType

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)

    def validate(self, id=None, label=None, folder_id=None, folder_label=None, dataset_id=None, dataset_name=None):
        logger.info('*' * 40 + self.__class__.__name__ + '*' * 40)
        logger.info('Lens start validation...')
        logger.info('validate lens type')
        assert self.type == 'lens'
        if id is not None:
            logger.info('validate lens id')
            assert self.id == id
        if label is not None:
            logger.info('validate lens label')
            assert self.label == label
        logger.info('validate lens allowPreview')
        assert self.allowPreview
        logger.info('validate lens permissions')
        self.permissions.validate()
        if folder_id is not None and folder_label is not None:
            logger.info('validate lens folder')
            self.folder.validate(id=folder_id, label=folder_label)
        if dataset_id is not None and dataset_name is not None:
            logger.info('validate lens dataset')
            self.dataset.validate(id=dataset_id, name=dataset_name)
        logger.info('Lens validation succeed!')
        logger.info('*' * 40 + self.__class__.__name__ + '*' * 40)


class WaveUser(JSONSerializable):
    def __init__(self, id='', name='', profilePhotoUrl=''):
        self.id = id
        self.name = name
        self.profilePhotoUrl = profilePhotoUrl

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)

class LensFile(JSONSerializable):
    def __init__(self, contentType='', fileLength=0, fileName='', id='', lastModifiedDate='', url=''):
        self.contentType = contentType
        self.fileLength = fileLength
        self.fileName = fileName
        self.id = id
        self.lastModifiedDate = lastModifiedDate
        self.url = url

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)

class Permissions(JSONSerializable):
    def __init__(self, manage=False, modify=False, view=False):
        self.manage = manage
        self.modify = modify
        self.view = view

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)

    def validate(self):
        logger.info('*' * 40 + self.__class__.__name__ + '*' * 40)
        logger.info('Permissions start validation...')
        logger.info('validate permissions')
        assert self.manage
        assert self.modify
        assert self.view
        logger.info('Permissions validation succeed!')
        logger.info('*' * 40 + self.__class__.__name__ + '*' * 40)

class LensState(JSONSerializable):
    def __init__(self, columns=None, query=None, **kwargs):
        if columns is None:
            columns = []
        # self.options = None
        if query is None:
            query = {}
        self.columns = [Column.from_json(column) for column in columns]
        self.query = Query.from_json(query)

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class Column(JSONSerializable):
    def __init__(self, header='', hidden=False, query=None, showBars=False, sort='None'):
        if query is None:
            query = {}
        self.header = header
        self.hidden = hidden
        self.query = Query.from_json(query)
        self.showBars = showBars
        self.sort = sort

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


# class LensVisualizationOptions(JSONSerializable):
#     def __init__(self):
#         # TODO
#         pass
#
#     @classmethod
#     def from_json(cls, json_str):
#         json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
#         json_dict = json.loads(json_str)
#         return cls(**json_dict)


class Query(JSONSerializable):
    def __init__(self, query='', version=''):
        self.query = query
        self.version = version

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)

########################################################################################################################
# dataset
########################################################################################################################
class DatasetRepresentation(JSONSerializable):
    def __init__(self,
                 assetSharingUrl='',
                 createdBy=None,
                 createdDate='',
                 currentVersionId='',
                 currentVersionUrl='',
                 description='',
                 folder=None,
                 id='',
                 label='',
                 lastAccessedDate='',
                 lastModifiedBy=None,
                 lastModifiedDate='',
                 lastQueriedDate='',
                 name='',
                 namespace='',
                 permissions=None,
                 type='',
                 url='',
                 versionsUrl='',
                 dataRefreshDate = None,
                 datasetType = None
                 ):

        if createdBy is None:
            createdBy = {}
        if folder is None:
            folder = {}
        if lastModifiedBy is None:
            lastModifiedBy = {}
        if permissions is None:
            permissions = {}

        if datasetType is None:
            datasetType = 'default'

        self.assetSharingUrl = assetSharingUrl
        self.createdBy = WaveUser.from_json(createdBy)
        self.createdDate = createdDate
        # self.currentVersionCreatedBy = None
        # self.currentVersionCreatedDate = None
        self.currentVersionId = currentVersionId
        # self.currentVersionLastModifiedBy = None
        # self.currentVersionLastModifiedDate = None
        self.currentVersionUrl = currentVersionUrl
        self.description = description
        self.folder = AssetReferenceRepresentation.from_json(folder)
        self.id = id
        self.label = label
        self.lastAccessedDate = lastAccessedDate
        self.lastModifiedBy = WaveUser.from_json(lastModifiedBy)
        self.lastModifiedDate = lastModifiedDate
        self.lastQueriedDate = lastQueriedDate
        self.name = name
        self.namespace = namespace
        self.permissions = Permissions.from_json(permissions)
        self.type = type
        self.url = url
        # self.userXmd = None
        self.versionsUrl = versionsUrl
        self.dataRefreshDate = dataRefreshDate

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)

    def validate(self, id=None, name=None, label=None, folder_id=None, folder_label=None):
        logger.info('*' * 40 + self.__class__.__name__ + '*' * 40)
        logger.info('start validation...')
        logger.info('validate dataset type')
        assert self.type == 'dataset'
        if id is not None:
            logger.info('validate lens id')
            assert self.id == id
        if name is not None:
            logger.info('validate lens name')
            assert self.name == name
        if label is not None:
            logger.info('validate lens label')
            assert self.label == label
        logger.info('validate dataset permissions')
        self.permissions.validate()
        if folder_id is not None and folder_label is not None:
            logger.info('validate lens folder')
            self.folder.validate(id=folder_id, label=folder_label)
        logger.info('validation succeed!')
        logger.info('*' * 40 + self.__class__.__name__ + '*' * 40)


class AssetReferenceRepresentation(JSONSerializable):
    def __init__(self, id='', label='', name='', namespace='', url=''):
        self.id = id
        self.label = label
        self.name = name
        self.namespace = namespace
        self.url = url

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)

    def validate(self, id=None, label=None, name=None):
        logger.info('*' * 40 + self.__class__.__name__ + '*' * 40)
        logger.info('AssetReferenceRepresentation start validation...')
        if id is not None:
            logger.info('validate folder id')
            assert self.id == id
        if label is not None:
            logger.info('validate folder label')
            assert self.label == label
        if name is not None:
            logger.info('validate folder name')
            assert self.name == name
        logger.info('AssetReferenceRepresentation validation succeed!')
        logger.info('*' * 40 + self.__class__.__name__ + '*' * 40)


########################################################################################################################
# dashboard
########################################################################################################################
class DashboardRepresentation(JSONSerializable):
    def __init__(self,
                 allowPreview=False,
                 mobileDisabled = False,
                 assetSharingUrl='',
                 createdBy=None,
                 createdDate='',
                 datasets=None,
                 description='',
                 files=None,
                 filesUrl='',
                 folder=None,
                 id='',
                 label='',
                 lastAccessedDate='',
                 lastModifiedBy=None,
                 lastModifiedDate='',
                 name='',
                 namespace='',
                 permissions=None,
                 refreshDate='',
                 state=None,
                 type='',
                 url=''
                 ):
        if createdBy is None:
            createdBy = {}
        if datasets is None:
            datasets = []
        if files is None:
            files = []
        if folder is None:
            folder = []
        if lastModifiedBy is None:
            lastModifiedBy = {}
        if permissions is None:
            permissions = {}
        if state is None:
            state = {}

        self.allowPreview = allowPreview

        self.mobileDisabled = mobileDisabled
        self.assetSharingUrl = assetSharingUrl
        self.createdBy = WaveUser.from_json(createdBy)
        self.createdDate = createdDate
        self.datasets = datasets
        self.description = description
        self.files = [LensFile.from_json(file_item) for file_item in files]
        self.filesUrl = filesUrl
        self.folder = AssetReferenceRepresentation.from_json(folder)
        self.id = id
        self.label = label
        self.lastAccessedDate = lastAccessedDate
        self.lastModifiedBy = WaveUser.from_json(lastModifiedBy)
        self.lastModifiedDate = lastModifiedDate
        self.name = name
        self.namespace = namespace
        self.permissions = Permissions.from_json(permissions)
        self.refreshDate = refreshDate
        self.state = DashboardState.from_json(state)
        self.type = type
        self.url = url

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)

    def validate(self, id=None, label=None, name=None, folder_id=None, folder_label=None):
        logger.info('*' * 40 + self.__class__.__name__ + '*' * 40)
        logger.info('DashboardRepresentation start validation...')

        logger.info('validate dashboard type')
        assert self.type == 'dashboard'

        if id is not None:
            logger.info('validate folder id')
            assert self.id == id

        if label is not None:
            logger.info('validate folder label')
            assert self.label == label

        if name is not None:
            logger.info('validate folder name')
            assert self.name == name

        logger.info('validate dashboard permissions')
        self.permissions.validate()

        if folder_id is not None and folder_label is not None:
            logger.info('validate lens folder')
            self.folder.validate(id=folder_id, label=folder_label)

        logger.info('validate dashboard layouts and widgets')
        assert (len(self.state.gridLayouts) == 1 and len(self.state.gridLayouts[0].pages) == 1)
        assert len(self.state.widgets) == len(self.state.gridLayouts[0].pages[0].widgets)
        widget_names = map(lambda x: x.name, self.state.gridLayouts[0].pages[0].widgets)
        assert all(map(lambda x: x in self.state.widgets, widget_names))

        logger.info('validate dashboard widgets and steps')
        widget_steps = set()
        for value in self.state.widgets.values():
            if 'step' in value['parameters']:
                widget_steps.add(value['parameters']['step'])
            elif 'text' in value['parameters'] and (value['parameters']['text']).find('step_') > 0 :
                text_value = value['parameters']['text']
                widget_steps.add(text_value[text_value.find('step_'): text_value.find('.')])

        #check for subset because some steps are intermediary steps which are not used in widgets
        assert widget_steps.issubset(set(self.state.steps))

        # TODO
        logger.info('DashboardRepresentation validation succeed!')
        logger.info('*' * 40 + self.__class__.__name__ + '*' * 40)

    def validate_detail(self, id=None, label=None, name=None, folder_id=None, folder_label=None):
        logger.info('*' * 40 + self.__class__.__name__ + '*' * 40)
        logger.info('DashboardRepresentation start validation...')

        logger.info('validate dashboard type')
        assert self.type == 'dashboard'

        if id is not None:
            logger.info('validate folder id')
            assert self.id == id

        if label is not None:
            logger.info('validate folder label')
            assert self.label == label

        if name is not None:
            logger.info('validate folder name')
            assert self.name == name

        logger.info('validate dashboard permissions')
        self.permissions.validate()

        if folder_id is not None and folder_label is not None:
            logger.info('validate lens folder')
            self.folder.validate(id=folder_id, label=folder_label)

        logger.info('validate dashboard layouts and widgets')
        assert (len(self.state.gridLayouts) == 1 and len(self.state.gridLayouts[0].pages) == 3)
        
        len_first_page_widgets = len(self.state.gridLayouts[0].pages[0].widgets)
        len_second_page_widgets = len(self.state.gridLayouts[0].pages[1].widgets)
        len_third_page_widgets = len(self.state.gridLayouts[0].pages[2].widgets)

        assert len(self.state.widgets) == len_first_page_widgets + len_second_page_widgets + len_third_page_widgets

        widget_names_one = map(lambda x: x.name, self.state.gridLayouts[0].pages[0].widgets)
        widget_names_two = map(lambda x: x.name, self.state.gridLayouts[0].pages[1].widgets)
        widget_names_three = map(lambda x: x.name, self.state.gridLayouts[0].pages[2].widgets)

        merged_widgets = widget_names_one + widget_names_two + widget_names_three

        assert all(map(lambda x: x in self.state.widgets, merged_widgets))

        logger.info('validate dashboard widgets and steps')
        widget_steps = set()
        for value in self.state.widgets.values():
            if 'step' in value['parameters']:
                widget_steps.add(value['parameters']['step'])
            elif 'text' in value['parameters'] and (value['parameters']['text']).find('step_') > 0 :
                text_value = value['parameters']['text']
                widget_steps.add(text_value[text_value.find('step_'): text_value.find('.')])

        #check for subset because some steps are intermediary steps which are not used in widgets
        assert widget_steps.issubset(set(self.state.steps))

        logger.info('DashboardRepresentation validation succeed!')
        logger.info('*' * 40 + self.__class__.__name__ + '*' * 40)

class DashboardState(JSONSerializable):
    def __init__(self,
                 dataSourceLinks=None,
                 # gridLayoutStyle=None,
                 gridLayouts=None,
                 layouts=None,
                 steps=None,
                 widgets=None,
                 widgetStyle=None,
                 filters = None
                 ):
        if dataSourceLinks is None:
            dataSourceLinks = []
        if gridLayouts is None:
            gridLayouts = []
        if layouts is None:
            layouts = []
        if steps is None:
            steps = {}
        if widgets is None:
            widgets = {}
        if widgetStyle is None:
            widgetStyle = {}
        if filters is None:
            filters= []
        self.dataSourceLinks = dataSourceLinks
        # self.gridLayoutStyle = None,
        self.gridLayouts = [GridLayoutRepresentation.from_json(gridLayout) for gridLayout in gridLayouts]
        self.layouts = [layout for layout in layouts]
        # TODO
        self.steps = steps
        self.widgets = widgets
        self.widgetStyle = GridLayoutWidgetStyleRepresentation.from_json(widgetStyle)
        self.filters = filters
    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class GridLayoutStyleRepresentation(JSONSerializable):
    def __init__(self,
                 alignmentX='',
                 alignmentY='',
                 backgroundColor='',
                 gutterColor = '',
                 cellSpacingY=0,
                 cellSpacingX=0,
                 documentId='',
                 fit=''
                 ):
        # self.gutterColor = None
        # self.image = None
        # self.widgetStyle = None
        self.alignmentX = alignmentX
        self.alignmentY = alignmentY
        self.backgroundColor = backgroundColor
        self.gutterColor = gutterColor
        self.cellSpacingY = cellSpacingY
        self.cellSpacingX = cellSpacingX
        self.documentId = documentId
        self.fit = fit

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class GridLayoutWidgetStyleRepresentation(JSONSerializable):
    def __init__(self,
                 backgroundColor='',
                 borderColor='',
                 borderEdges=None,
                 borderRadius=0,
                 borderWidth=1
                 ):
        if borderEdges is None:
            borderEdges = []

        self.backgroundColor = backgroundColor
        self.borderColor = borderColor
        self.borderEdges = borderEdges
        self.borderRadius = borderRadius
        self.borderWidth = borderWidth
        # self.bottomPadding = None
        # self.leftPadding = None
        # self.rightPadding = None
        # self.topPadding = None

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class GridLayoutRepresentation(JSONSerializable):
    def __init__(self,
                 maxWidth=1,
                 name='',
                 numColumns=1,
                 pages=None,
                 selectors=None,
                 style=None,
                 rowHeight = None,
                 version=0.1
                 ):
        if pages is None:
            pages = []
        if selectors is None:
            selectors = []
        if style is None:
            style = {}

        self.maxWidth = maxWidth
        self.name = name
        self.numColumns = numColumns
        self.pages = [GridLayoutPageRepresentation.from_json(page) for page in pages]

        # self.rowHeight = None
        self.selectors = selectors
        self.style = GridLayoutStyleRepresentation.from_json(style)
        self.version = version
        # self.widgetStyle = None

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class GridLayoutPageRepresentation(JSONSerializable):

    def __init__(self, widgets=None, name = None, label = None):
        if widgets is None:
            widgets = []
        if name is None:
            name = ''
        if label is None:
            label = ''
        self.widgets = [GridLayoutWidgetRepresentation.from_json(widget) for widget in widgets]
        self.name = name
        self.label = label

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class GridLayoutWidgetRepresentation(JSONSerializable):
    def __init__(self,
                 colspan=1,
                 column=1,
                 name='',
                 row=1,
                 rowspan=1,
                 widgetStyle=None
                 ):
        if widgetStyle is None:
            widgetStyle = {}

        # self.backgroundImage = None
        self.colspan = colspan
        self.column = column
        self.name = name
        self.row = row
        self.rowspan = rowspan
        self.widgetStyle = GridLayoutWidgetStyleRepresentation.from_json(widgetStyle)

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class Layout(JSONSerializable):
    def __init__(self, device='', orientation='', pages=None, version=0.1):
        if pages is None:
            pages = []
        self.device = device
        self.orientation = orientation
        self.pages = [LayoutPage.from_json(page) for page in pages]
        self.version = version

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class LayoutPage(JSONSerializable):
    def __init__(self, rows=None):
        if rows is None:
            rows = []
        self.rows = rows

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class DashboardWidget(JSONSerializable):
    def __init__(self, parameters=None, position=None, type=''):
        if parameters is None:
            parameters = {}
        if position is None:
            position = {}

        # TODO
        self.parameters = parameters
        self.position = WidgetPosition.from_json(position)
        self.type = type

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class WidgetPosition(JSONSerializable):
    def __init__(self, h='', w='', x=0, y=0, zIndex=0):
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        self.zIndex = zIndex

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class WidgetParameter(JSONSerializable):
    def __init__(self, type='', obj=None):
        if obj is None:
            obj = {}

    @classmethod
    def from_json(cls, type, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(type, json_dict)


########################################################################################################################
# dashboard for PATCH and POST Request Body
########################################################################################################################
class DashboardInputRepresentation(JSONSerializable):
    def __init__(self, description='', folder=None, label='', name='', state=None):
        if folder is None:
            folder = {}
        if state is None:
            state = {}

        self.description = description
        self.folder = AssetReferenceInputRepresentation.from_json(folder)
        self.label = label
        self.name = name
        self.state = DashboardStateInputRepresentation.from_json(state)

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class AssetReferenceInputRepresentation(JSONSerializable):
    def __init__(self, id='', name='', namespace=''):
        self.id = id
        self.name = name
        self.namespace = namespace

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class DashboardStateInputRepresentation(JSONSerializable):
    def __init__(self,
                 gridLayoutStyle=None,
                 gridLayouts=None,
                 layouts=None,
                 steps=None,
                 widgets=None,
                 widgetStyle=None
                 ):
        if gridLayoutStyle is None:
            gridLayoutStyle = {}
        if gridLayouts is None:
            gridLayouts = []
        if layouts is None:
            layouts = []
        if steps is None:
            steps = {}
        if widgets is None:
            widgets = {}
        if widgetStyle is None:
            widgetStyle = {}

        self.gridLayoutStyle = GridLayoutStyleInputRepresentation.from_json(gridLayoutStyle)
        self.gridLayouts = [GridLayoutInputRepresentation.from_json(gridLayout) for gridLayout in gridLayouts]
        self.layouts = [LayoutInputRepresentation.from_json(layout) for layout in layouts]
        self.widgetStyle = GridLayoutWidgetStyleInputRepresentation.from_json(widgetStyle)
        # TODO
        self.steps = steps
        self.widgets = widgets

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class GridLayoutWidgetStyleInputRepresentation(JSONSerializable):
    def __init__(self,
                 backgroundColor='',
                 borderColor='',
                 borderEdges=None,
                 borderRadius=0,
                 borderWidth=1,
                 bottomPadding=0,
                 leftPadding=0,
                 rightPadding=0,
                 topPadding=0
                 ):
        if borderEdges is None:
            borderEdges = []

        self.backgroundColor = backgroundColor
        self.borderColor = borderColor
        self.borderEdges = borderEdges
        self.borderRadius = borderRadius
        self.borderWidth = borderWidth
        self.bottomPadding = bottomPadding
        self.leftPadding = leftPadding
        self.rightPadding = rightPadding
        self.topPadding = topPadding

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class GridLayoutStyleInputRepresentation(JSONSerializable):
    def __init__(self,
                 backgroundColor='',
                 cellSpacingY=0,
                 cellSpacingX=0,
                 documentId='',
                 gutterColor='',
                 image=None,
                 widgetStyle=None
                 ):
        if image is None:
            image = {}
        if widgetStyle is None:
            widgetStyle = {}

        self.backgroundColor = backgroundColor
        self.cellSpacingY = cellSpacingY
        self.cellSpacingX = cellSpacingX
        self.documentId = documentId
        self.gutterColor = gutterColor
        self.image = AssetReferenceRepresentation.from_json(image)
        self.widgetStyle = GridLayoutWidgetStyleInputRepresentation.from_json(widgetStyle)

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class GridLayoutInputRepresentation(JSONSerializable):
    def __init__(self,
                 maxWidth=1,
                 name='',
                 numColumns=1,
                 pages=None,
                 rowHeight=None,
                 selectors=None,
                 style=None,
                 version=0.1
                 ):
        if pages is None:
            pages = []
        if rowHeight is None:
            rowHeight = {},
        if selectors is None:
            selectors = []
        if style is None:
            style = {}

        self.maxWidth = maxWidth
        self.name = name
        self.numColumns = numColumns
        self.pages = [GridLayoutPageInputRepresentation.from_json(page) for page in pages]
        self.rowHeight = None
        self.selectors = selectors
        self.style = GridLayoutStyleInputRepresentation.from_json(style)
        self.version = version
        self.widgetStyle = None

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class GridLayoutPageInputRepresentation(JSONSerializable):
    def __init__(self, widgets=None):
        if widgets is None:
            widgets = []
        self.widgets = [GridLayoutWidgetInputRepresentation.from_json(widget) for widget in widgets]

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class GridLayoutWidgetInputRepresentation(JSONSerializable):
    def __init__(self,
                 backgroundImage='',
                 colspan=1,
                 column=1,
                 name='',
                 row=1,
                 rowspan=1,
                 widgetStyle=None
                 ):
        if widgetStyle is None:
            widgetStyle = {}

        self.backgroundImage = backgroundImage
        self.colspan = colspan
        self.column = column
        self.name = name
        self.row = row
        self.rowspan = rowspan
        self.widgetStyle = GridLayoutWidgetStyleInputRepresentation.from_json(widgetStyle)

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class LayoutInputRepresentation(JSONSerializable):
    def __init__(self, device='', orientation='', pages=None, version=0.1):
        if pages is None:
            pages = []
        self.device = device
        self.orientation = orientation
        self.pages = [LayoutPageInputRepresentation.from_json(page) for page in pages]
        self.version = version

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class LayoutPageInputRepresentation(JSONSerializable):
    def __init__(self, rows=None):
        if rows is None:
            rows = []
        self.rows = rows

    @classmethod
    def from_json(cls, json_str):
        json_str = json.dumps(json_str) if not isinstance(json_str, str) else json_str
        json_dict = json.loads(json_str)
        return cls(**json_dict)
