set datafile separator ','
# set key autotitle columnhead

plot "VAASRCNN2__c_dropout_p_0.5__f_dropout_p_0.5__feature_retrained-wav2vec_features-c__fold_id_0__obj_voice_cmd.csv" using 1:2 with lines, \
"VAASRCNN2__c_dropout_p_0.5__f_dropout_p_0.5__feature_retrained-wav2vec_features-z__fold_id_0__obj_voice_cmd.csv" using 1:2 with lines, \
"VAASRCNN2__c_dropout_p_0.5__f_dropout_p_0.5__feature_wav2vec_features-c__fold_id_0__obj_voice_cmd.csv" using 1:2 with lines, \
"VAASRCNN2__c_dropout_p_0.5__f_dropout_p_0.5__feature_wav2vec_features-z__fold_id_0__obj_voice_cmd.csv" using 1:2 with lines, \
"VAASRCNN3__c_dropout_p_0.5__f_dropout_p_0.5__feature_wav2vec_features-c__fold_id_0__obj_voice_cmd.csv" using 1:2 with lines \

#"VAASRCNN2__c_dropout_p_0.5__f_dropout_p_0.5__feature_retrained-wav2vec_features-c__fold_id_0__obj_voice_cmd.csv" using 1:2 with lines,
#"VAASRCNN2__c_dropout_p_0.5__f_dropout_p_0.5__feature_retrained-wav2vec_features-z__fold_id_0__obj_voice_cmd.csv" using 1:2 with lines,
#"VAASRCNN2__c_dropout_p_0.5__f_dropout_p_0.5__feature_wav2vec_features-c__fold_id_0__obj_voice_cmd.csv" using 1:2 with lines,
#"VAASRCNN2__c_dropout_p_0.5__f_dropout_p_0.5__feature_wav2vec_features-z__fold_id_0__obj_voice_cmd.csv" using 1:2 with lines


# train acc: 51
# test loss: 34
# test acc: 2