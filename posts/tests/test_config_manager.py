from posts.singletons.config_manager import ConfigManager

config1 = ConfigManager()
config2 = ConfigManager()


assert config1 is config2  # Both instances should be the same
config1.set_setting("DEFAULT_PAGE_SIZE", 50)
assert config2.get_setting("DEFAULT_PAGE_SIZE") == 50
