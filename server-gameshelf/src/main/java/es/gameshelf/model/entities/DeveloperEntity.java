package es.gameshelf.model.entities;

import es.gameshelf.domain.abstracts.Classification;
import es.gameshelf.model.entities.abstracts.ClassificationEntity;
import jakarta.persistence.*;

import java.util.Set;

/**
 * @author Nabil L. A. @nalleon
 */
@Entity
@Table(name="developers")
@NamedQuery(name="DeveloperEntity.findAll", query="SELECT r FROM DeveloperEntity r")
public class DeveloperEntity extends ClassificationEntity {


    @ManyToMany(mappedBy = "developerEntitySet", cascade = CascadeType.PERSIST,fetch = FetchType.LAZY)
    Set<GameEntity> games;

    /**
     * Default constructor of the class
     */
    public DeveloperEntity() {
    }

    /**
     * Constructor of the class
     * @param id of the developer
     */
    public DeveloperEntity(int id) {
        super(id);
    }

    /**
     * Constructor of the class
     * @param name of the developer
     */
    public DeveloperEntity(String name) {
        super(name);
    }

    /**
     * Full constructor of the class
     * @param id of the developer
     * @param name of the developer
     */
    public DeveloperEntity(int id, String name) {
        super(id, name);
    }
}
