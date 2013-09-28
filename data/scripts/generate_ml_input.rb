class String
  def underscore
    self.gsub(/::/, '/').
    gsub(/([A-Z]+)([A-Z][a-z])/,'\1_\2').
    gsub(/([a-z\d])([A-Z])/,'\1_\2').
    tr("-", "_").
    downcase
  end
end

def generate_ml_input(folder_name)
  Dir.glob("#{folder_name}/*") do |file|
    next if file == '.' or file == '..'
    if File.directory?(file)
      generate_ml_input(file)
    else
      count_classes_in_file(file)
    end
  end
end

def count_classes_in_file(file)
    class_map = {}
    text = IO.read(file).force_encoding("ISO-8859-1").encode("utf-8", replace: nil)
    classes = text.scan(/class="([\w\-\s]+)"/).map { |a| a[0].underscore.gsub("_", " ").gsub("-", " ").split(" ") }.flatten(1)

    classes.each do |c|
      class_map[c] = class_map[c].nil? ? 1 : class_map[c] + 1
    end

    puts "file name: #{file}"
    puts "classes: #{class_map.sort_by {|k,v| v }}"
end

if !(ARGV.first)
  puts "please provide the name of the folder containing websites"
  exit
end

generate_ml_input(ARGV.first)
