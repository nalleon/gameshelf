package es.gameshelf.domain.services;

import es.gameshelf.domain.Developer;
import es.gameshelf.domain.interfaces.repository.IDeveloperRepository;
import es.gameshelf.domain.interfaces.service.IDeveloperService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
@Service
public class DeveloperService implements IDeveloperService {
    /**
     * Properties
     */
    IDeveloperRepository repository;

    /**
     * Setter for the autowired service
     * @param repository of the service
     */
    @Autowired
    public void setRepository(IDeveloperRepository repository) {
        this.repository = repository;
    }

    @Override
    public Developer add(String name) {
        Developer item = new Developer();
        item.setName(name);
        return repository.save(item);
    }

    @Override
    public List<Developer> findAll() {
        return repository.findAll();
    }

    @Override
    public Developer findById(Integer id) {
        return repository.findById(id);
    }

    @Override
    public Developer findByName(String name) {
        return repository.findByName(name);
    }

    @Override
    public boolean delete(Integer id) {
        return repository.delete(id);
    }

    @Override
    public Developer update(Integer id, String name) {
        Developer item = new Developer(id);
        item.setName(name);
        return repository.save(item);    }
}
