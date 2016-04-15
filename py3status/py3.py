PY3_CACHE_FOREVER = -1


class Py3:
    """
    Helper object that gets injected as self.py3 into Py3status
    modules that have not got that attribute set already.

    This allows functionality like:
        User notifications
        Forcing module to update (even other modules)
        Triggering events for modules
    """

    CACHE_FOREVER = PY3_CACHE_FOREVER

    def __init__(self, module):
        self._module = module

    def update(self, module_name=None):
        """
        Update a module.  If module_name is supplied the module of that
        name is updated.  Otherwise the module calling is updated.
        """
        if not module_name:
            return self._module.force_update()
        else:
            module = self.get_module_info(module_name).get('module')
            if module:
                module.force_update()

    def get_module_info(self, module_name):
        """
        Helper function to get info for named module.
        Info comes back as a dict containing.

        'module': the instance of the module,
        'position': list of places in i3bar, usually only one item
        'type': module type py3status/i3status
        """
        return self._module._py3_wrapper.output_modules.get(module_name)

    def trigger_event(self, module_name, event):
        """
        Trigger the event on named module
        """
        if module_name:
            self._module._py3_wrapper.events_thread.process_event(
                module_name, event)

    def notify_user(self, msg, level='info'):
        """
        Send notification to user.
        level can be 'info', 'error' or 'warning'
        """
        self._module._py3_wrapper.notify_user(msg, level=level)

    def register_content_function(self, content_function):
        """
        Register a function that can be called to discover what modules a
        container is displaying.  This is used to determine when updates need
        passing on to the container and also when modules can be put to sleep.

        the function must return a set of module names that are being
        displayed.

        Note: This function should only be used by containers.
        """
        my_info = self.get_module_info(self._module.module_full_name)
        my_info['content_function'] = content_function
