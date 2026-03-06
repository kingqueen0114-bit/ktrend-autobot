import ConfigStore from 'configstore';
const sanityEnv = (process.env.SANITY_INTERNAL_ENV || '').toLowerCase();
const configName = sanityEnv && sanityEnv !== 'production' ? `sanity-${sanityEnv}` : 'sanity';
const defaults = {};
let config;
export const getUserConfig = ()=>{
    if (!config) {
        config = new ConfigStore(configName, defaults, {
            globalConfigPath: true
        });
    }
    return config;
};

//# sourceMappingURL=getUserConfig.js.map