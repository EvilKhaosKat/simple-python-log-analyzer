class FiltersSequence:
    filters = []
    is_html = False

    def __init__(self, filters, is_html=False):
        self.filters = filters
        self.is_html = is_html
        #TODO sequence of filters in order of it's 'weight'

    def apply(self, data_source):
        result = data_source
        for filter in self.filters:
            print('Performing ' + str(filter))
            result = filter.apply(result)
            #print("len:" + str(len(result)))

        return result
