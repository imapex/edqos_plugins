module.exports = function(grunt) {

  grunt.initConfig({
    lambda_invoke: {
      default: {
        options: {
        }
      }
    },
    lambda_package: {
      default: {
        options: {
        }
      }
    },
    lambda_deploy: {
      default: {
        arn: 'ARN',
        options: {
        }
      }
    },
  });

  grunt.loadNpmTasks('grunt-aws-lambda');

  grunt.registerTask('default', ['lambda_invoke']);
  grunt.registerTask('build', ['lambda_package']);
  grunt.registerTask('deploy', ['lambda_deploy']);

};
