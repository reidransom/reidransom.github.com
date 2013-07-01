module.exports = function(grunt) {
    grunt.initConfig({
        watch: {
            files: ['public/assets/less/*.less'],
            tasks: 'less:dev'
        },

        less: {
            dev: {
                files: {
                    'public/assets/css/style.css': 'public/assets/less/style.less'
                }
            }
        }
    
    });
    
    grunt.registerTask('default', 'less:dev');

    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-watch');
}