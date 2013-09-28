def generate_ml_input(folder_name)
  class_map = {}

  Dir.open folder_name do |dir|
    dir.each do |file|
      text = file.read
      classes = text.scan(/class="([\w\-\s]+)"/).map { |a| a[0].split(" ") }.flatten(1)

      classes.each do |c|
        class_map[c] = class_map[c].nil? ? 1 : class_map[c] + 1
      end
    end
  end

  puts class_map
end

if !(ARGV.first)
  puts "please provide the name of the folder containing websites"
  exit
end

generate_ml_input(ARGV.first)
