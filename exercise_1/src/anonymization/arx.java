package anonymization;
import org.apache.commons.lang.ObjectUtils;
import org.deidentifier.arx.*;
import org.deidentifier.arx.criteria.KAnonymity;
import org.deidentifier.arx.metric.Metric;

import javax.lang.model.type.NullType;
import javax.management.Attribute;
import java.io.IOException;
import java.nio.charset.Charset;

public class arx {
        public static void main(String[] args) throws IOException {
            Data data = Data.create("exercise_1/data/adult_header.data", Charset.defaultCharset(), ',');

            String[] insensitive = new String[]{"capital-loss", "education-num",
                    "capital-gain", "hours-per-week", "target", "fnlwgt"};

            String[] cols = new String[]{"age", "sex", "native-country", "race", "occupation",
                    "education", "marital-status", "workclass", "relationship"};

            for (int i = 0; i < insensitive.length; i++) {
                data.getDefinition().setAttributeType(insensitive[i], AttributeType.INSENSITIVE_ATTRIBUTE);
            }

            for (int i = 0; i < cols.length; i++) {
                data.getDefinition().setAttributeType(cols[i], AttributeType.QUASI_IDENTIFYING_ATTRIBUTE);
                String hierPath = "exercise_1/data/anonymization/hierarchy/adult_hierarchy_"+cols[i]+".csv";
                AttributeType.Hierarchy hierarchy = AttributeType.Hierarchy.create(hierPath,
                        Charset.defaultCharset(),
                        ';');
                data.getDefinition().setAttributeType(cols[i], hierarchy);
            }

        Integer[] ks = new Integer[]{1,5,10,25,50,75,100};
        for (int i = 0; i < ks.length; i++) {
            int k = ks[i];
            System.out.println("Doing k-Anonymity with k: "+k+" ...");
            ARXConfiguration config = ARXConfiguration.create();
            //config.setQualityModel(Metric.createLossMetric());
            config.addPrivacyModel(new KAnonymity(k));
            config.setSuppressionLimit(1d);

            ARXAnonymizer anonymizer = new ARXAnonymizer();

            ARXResult result = anonymizer.anonymize(data, config);
            DataHandle handle = result.getOutput();
            String out = "exercise_1/data/anonymization/k-anonymity/anonymized_k"+k+".data";
            handle.save(out, ',');
            handle.release();
            data.getHandle().release();
            System.out.println("--- done with k: "+k);

        }

    }
}
